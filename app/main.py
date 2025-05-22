from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np
import onnxruntime as ort
import joblib
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import redis

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
MODEL_PATH = os.getenv("MODEL_PATH")
JWT_SECRET = os.getenv("JWT_SECRET")

# Initialize FastAPI app
app = FastAPI()

# Load ONNX model and encoder
onnx_session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
encoder = joblib.load('/Users/mac/Desktop/FRAUD DETECTION/onehot_encoder.pkl')

# Initialize database connection
conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

# Initialize Redis client
redis_client = redis.StrictRedis.from_url(REDIS_URL)

# Define input schema
class Transaction(BaseModel):
    TransactionAmount: float
    CustomerAge: int
    TransactionDuration: float
    LoginAttempts: int
    AccountBalance: float
    TransactionType: str
    Location: str
    Channel: str
    CustomerOccupation: str
    user_primary_location: str

# API for real-time data ingestion
@app.post("/transactions/ingest")
async def ingest_transaction(transaction: Transaction):
    try:
        # Save transaction to the database
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO transactions (amount, location, event_time, is_fraud, fraud_probability)
                VALUES (%s, %s, NOW(), NULL, NULL)
                """,
                (transaction.TransactionAmount, transaction.Location),
            )
        conn.commit()
        return {"message": "Transaction ingested successfully", "data": transaction.dict()}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# API for model inference
@app.post("/transactions/score")
async def score_transaction(transaction: Transaction):
    try:
        # Prepare input for the model
        numeric_features = np.array([
            transaction.TransactionAmount,
            transaction.CustomerAge,
            transaction.TransactionDuration,
            transaction.LoginAttempts,
            transaction.AccountBalance,
        ]).reshape(1, -1)

        categorical_features = encoder.transform([[
            transaction.TransactionType,
            transaction.Location,
            transaction.Channel,
            transaction.CustomerOccupation,
            transaction.user_primary_location,
        ]])

        # Combine numeric and categorical features
        features = np.hstack((numeric_features, categorical_features)).astype(np.float32)

        # Predict fraud probability using ONNX model
        input_name = onnx_session.get_inputs()[0].name
        output_name = onnx_session.get_outputs()[0].name
        fraud_probability = onnx_session.run([output_name], {input_name: features})[0][0][1]  # Probability of class 1
        is_fraud = fraud_probability >= 0.3  # Use the custom threshold of 0.3

        # Save results to the database
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO transactions (amount, location, event_time, is_fraud, fraud_probability)
                VALUES (%s, %s, NOW(), %s, %s)
                """,
                (transaction.TransactionAmount, transaction.Location, is_fraud, fraud_probability),
            )
        conn.commit()

        return {"fraud_probability": fraud_probability, "is_fraud": is_fraud}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")