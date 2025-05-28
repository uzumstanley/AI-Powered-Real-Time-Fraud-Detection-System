# API Endpoints

from fastapi import APIRouter, Depends, WebSocket, BackgroundTasks
from pydantic import BaseModel
from datetime import datetime
import numpy as np

# Import dependencies from other modules
from .main import get_current_user, session, insert_transaction, insert_alert, redis_client

router = APIRouter()

class Transaction(BaseModel):
    id: str
    account: str
    features: list[float]  # flattened vector
    time: datetime

@router.post("/transactions/score")
async def score_transaction(
    tx: Transaction,
    user: str = Depends(get_current_user),
    bg: BackgroundTasks = None
):
    # 1. Prepare input
    inp = np.array([tx.features], dtype=np.float32)
    # 2. Inference
    score = session.run(None, {session.get_inputs()[0].name: inp})[0][0]
    is_fraud = bool(score > 0.5)  # threshold
    # 3. Persist in background
    bg.add_task(insert_transaction, {
        "id": tx.id, "account": tx.account,
        "features": tx.features, "score": score,
        "is_fraud": is_fraud, "time": tx.time
    })
    if is_fraud:
        bg.add_task(insert_alert, tx.id)
    # 4. Cache latest score
    redis_client.hset(f"user:{tx.account}", mapping={"last_score": score})

    return {"score": score, "is_fraud": is_fraud}

@router.post("/transactions/ingest")
async def ingest_transaction(tx: Transaction):
    # Could enqueue to Redis Stream or Kafka here
    redis_client.xadd("transactions", tx.dict())
    return {"status": "queued"}

@router.websocket("/ws/alerts")
async def alerts_ws(ws: WebSocket):
    await ws.accept()
    pubsub = redis_client.pubsub()
    pubsub.subscribe("alerts")
    for msg in pubsub.listen():
        if msg["type"] == "message":
            await ws.send_text(msg["data"])