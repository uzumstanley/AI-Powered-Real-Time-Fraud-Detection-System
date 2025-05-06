import os
import logging
import logging.config
from datetime import datetime, timedelta

import redis
import onnxruntime as ort
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends, BackgroundTasks, WebSocket, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import numpy as np

# ── Load environment variables ────────────────────────────────────────────────
load_dotenv()

REDIS_URL    = os.getenv("REDIS_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET   = os.getenv("JWT_SECRET")
MODEL_PATH   = os.getenv("MODEL_PATH", "/Users/mac/Desktop/FRAUD DETECTION/app/fraud_detector_1bit.onnx")

if not all([REDIS_URL, DATABASE_URL, JWT_SECRET]):
    raise RuntimeError("Missing one of REDIS_URL, DATABASE_URL, or JWT_SECRET in environment")

# ── Configure Logging ────────────────────────────────────────────────────────
logging.config.dictConfig({
    "version": 1,
    "formatters": {
        "default": {"format": "%(asctime)s %(levelname)s %(name)s: %(message)s"}
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "default"}
    },
    "root": {"handlers": ["console"], "level": "INFO"}
})
logger = logging.getLogger(__name__)

# ── Initialize FastAPI ──────────────────────────────────────────────────────
app = FastAPI()

# ── JWT Auth Setup ──────────────────────────────────────────────────────────
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_token(subject: str) -> str:
    payload = {"sub": subject, "exp": datetime.utcnow() + timedelta(hours=2)}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication credentials")

# ── Redis Client ────────────────────────────────────────────────────────────
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# ── ONNX Model Loading ───────────────────────────────────────────────────────
session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])

@app.on_event("startup")
async def startup_event():
    # Warm up the ONNX session once
    dummy = np.zeros((1, session.get_inputs()[0].shape[1]), dtype=np.float32)
    session.run(None, {session.get_inputs()[0].name: dummy})
    logger.info("ONNX model loaded and warmed up.")

# ── Database Connection ─────────────────────────────────────────────────────
conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
conn.autocommit = True

def insert_transaction(tx: dict):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO transactions
            (transaction_id, account_id, features, score, is_fraud, event_time)
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (tx["id"], tx["account"], tx["features"], tx["score"], tx["is_fraud"], tx["time"])
        )

def insert_alert(tx_id: str):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO alerts (transaction_id, alert_type, created_at)
            VALUES (%s, %s, NOW())
            """,
            (tx_id, "HIGH_RISK")
        )
        # also push to Redis stream for WebSocket
        redis_client.xadd("alerts", {"transaction_id": tx_id})

# ── Request & Data Models ───────────────────────────────────────────────────
class Transaction(BaseModel):
    id: str
    account: str
    features: list[float]
    time: datetime

# ── Exception Handling ──────────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

# ── API Endpoints ────────────────────────────────────────────────────────────
@app.post("/transactions/ingest")
async def ingest_transaction(tx: Transaction):
    """Queue raw transaction for processing."""
    redis_client.xadd("transactions", tx.dict())
    return {"status": "queued"}

@app.post("/transactions/score")
async def score_transaction(
    tx: Transaction,
    user: str = Depends(get_current_user),
    bg: BackgroundTasks = None
):
    """Run fraud scoring and persist results."""
    arr = np.array([tx.features], dtype=np.float32)
    score = float(session.run(None, {session.get_inputs()[0].name: arr})[0][0])
    is_fraud = score > 0.5

    # Persist transaction & alert asynchronously
    bg.add_task(insert_transaction, {
        "id": tx.id, "account": tx.account,
        "features": tx.features, "score": score,
        "is_fraud": is_fraud, "time": tx.time
    })
    if is_fraud:
        bg.add_task(insert_alert, tx.id)

    # Update Redis cache
    redis_client.hset(f"user:{tx.account}", mapping={"last_score": score})

    return {"score": score, "is_fraud": is_fraud}

@app.websocket("/ws/alerts")
async def alerts_ws(ws: WebSocket):
    """Push new alerts to connected clients."""
    await ws.accept()
    pubsub = redis_client.pubsub()
    pubsub.subscribe("alerts")
    for msg in pubsub.listen():
        if msg["type"] == "message":
            await ws.send_text(msg["data"])

# ── Health Check ────────────────────────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok", "model_loaded": True}

