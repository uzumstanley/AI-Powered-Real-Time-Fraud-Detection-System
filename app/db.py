# Database Connection

import os
import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(os.getenv("DATABASE_URL"), cursor_factory=RealDictCursor)  # :contentReference[oaicite:12]{index=12}
conn.autocommit = True

def insert_transaction(tx):
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO transactions
               (transaction_id, account_id, features, score, is_fraud, event_time)
               VALUES (%s,%s,%s,%s,%s,%s)""",
            (tx["id"], tx["account"], tx["features"], tx["score"], tx["is_fraud"], tx["time"])
        )

def insert_alert(tx_id, score):
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO alerts (transaction_id, alert_type, created_at)
               VALUES (%s, %s, NOW())""",
            (tx_id, "HIGH_RISK")
        )
