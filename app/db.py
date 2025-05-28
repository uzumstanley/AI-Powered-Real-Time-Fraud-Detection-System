# Database Connection

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from .main import redis_client  # Import Redis client for alert integration

# Ensure DATABASE_URL is set
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")

# Establish database connection
try:
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    conn.autocommit = True
except psycopg2.OperationalError as e:
    raise RuntimeError(f"Failed to connect to the database: {e}")

def insert_transaction(tx):
    """Insert a transaction into the database."""
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO transactions
               (transaction_id, account_id, features, score, is_fraud, event_time)
               VALUES (%s,%s,%s,%s,%s,%s)""",
            (tx["id"], tx["account"], tx["features"], tx["score"], tx["is_fraud"], tx["time"])
        )

def insert_alert(tx_id, score):
    """Insert an alert into the database and push to Redis."""
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO alerts (transaction_id, alert_type, created_at)
               VALUES (%s, %s, NOW())""",
            (tx_id, "HIGH_RISK")
        )
    # Push alert to Redis for WebSocket notifications
    redis_client.xadd("alerts", {"transaction_id": tx_id, "score": score})