import os
import logging
import logging.config
from datetime import datetime, timedelta, timezone

import redis
import json
import onnxruntime as ort
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Request, Depends, BackgroundTasks, WebSocket, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
import numpy as np
from contextlib import asynccontextmanager

# Initialize FastAPI app with lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager to initialize and clean up resources."""
    # Initialize ONNX model session
    app.state.session = ort.InferenceSession(os.getenv("MODEL_PATH", "fraud_detector_1bit.onnx"))
    print("ONNX model session initialized.")

    # Initialize database connection
    app.state.conn = psycopg2.connect(os.getenv("DATABASE_URL"), cursor_factory=RealDictCursor)
    print("Database connection established.")

    # Initialize Redis client
    app.state.redis_client = redis.StrictRedis.from_url(os.getenv("REDIS_URL"))
    print("Redis client initialized.")

    # Yield control to the application
    yield

    # Cleanup resources
    app.state.conn.close()
    print("Database connection closed.")

app = FastAPI(lifespan=lifespan)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define get_current_user
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET", "your_default_secret"), algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Define the Transaction model
class Transaction(BaseModel):
    id: str
    account: str
    features: List[float]  # List of numerical features
    time: str  # ISO 8601 timestamp

# ── API Endpoints ────────────────────────────────────────────────────────────
@app.post("/transactions/score")
async def score_transaction(
    tx: Transaction,
    user: str = Depends(get_current_user),
    bg: BackgroundTasks = None
):
    """Run fraud scoring and persist results."""
    session = app.state.session
    conn = app.state.conn
    redis_client = app.state.redis_client

    arr = np.array([tx.features], dtype=np.float32)
    score = float(session.run(None, {session.get_inputs()[0].name: arr})[0][0])
    is_fraud = score > 0.5

    # Persist transaction & alert asynchronously
    def insert_transaction(tx: dict):
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO transactions
                (transaction_id, account_id, features, score, is_fraud, event_time)
                VALUES (%s,%s,%s,%s,%s,%s)
                """,
                (
                    tx["id"],
                    tx["account"],
                    json.dumps(tx["features"]),  # Convert features to JSON
                    tx["score"],
                    tx["is_fraud"],
                    tx["time"]
                )
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
            redis_client.xadd("alerts", {"transaction_id": tx_id})

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