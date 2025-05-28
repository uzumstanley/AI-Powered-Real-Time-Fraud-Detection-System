from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
<<<<<<< HEAD
from typing import List
import numpy as np
import onnxruntime as ort
=======
import numpy as np
>>>>>>> 39e0989 (Initial commit: Add complete AI-powered real-time fraud detection system)
import joblib
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import redis
<<<<<<< HEAD

=======
from fastapi.middleware.cors import CORSMiddleware


>>>>>>> 39e0989 (Initial commit: Add complete AI-powered real-time fraud detection system)
# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
<<<<<<< HEAD
MODEL_PATH = os.getenv("MODEL_PATH")
JWT_SECRET = os.getenv("JWT_SECRET")
=======
>>>>>>> 39e0989 (Initial commit: Add complete AI-powered real-time fraud detection system)

# Initialize FastAPI app
app = FastAPI()

<<<<<<< HEAD
# Load ONNX model and encoder
onnx_session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
encoder = joblib.load('/Users/mac/Desktop/FRAUD DETECTION/onehot_encoder.pkl')

=======
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost:3000"] for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Isolation Forest model and encoder
iso_forest = joblib.load('/Users/mac/Desktop/FRAUD DETECTION/iso_forest_model.pkl')
encoder = joblib.load('/Users/mac/Desktop/FRAUD DETECTION/onehot_encoder.pkl')

>>>>>>> 39e0989 (Initial commit: Add complete AI-powered real-time fraud detection system)
# Initialize database connection
conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

# Initialize Redis client
redis_client = redis.StrictRedis.from_url(REDIS_URL)

<<<<<<< HEAD
# Define input schema
class Transaction(BaseModel):
=======
# Define input schema (all features used in training)
class Transaction(BaseModel):
    account_id: str
>>>>>>> 39e0989 (Initial commit: Add complete AI-powered real-time fraud detection system)
    TransactionAmount: float
    CustomerAge: int
    TransactionDuration: float
    LoginAttempts: int
    AccountBalance: float
<<<<<<< HEAD
=======
    user_transaction_count: float
    user_avg_transaction_amount: float
    deviation_from_user_avg: float
    transaction_hour: int
    transaction_day_of_week: int
>>>>>>> 39e0989 (Initial commit: Add complete AI-powered real-time fraud detection system)
    TransactionType: str
    Location: str
    Channel: str
    CustomerOccupation: str
    user_primary_location: str
<<<<<<< HEAD
=======
    is_unusual_location: str
>>>>>>> 39e0989 (Initial commit: Add complete AI-powered real-time fraud detection system)

# API for real-time data ingestion
@app.post("/transactions/ingest")
async def ingest_transaction(transaction: Transaction):
    try:
<<<<<<< HEAD
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
=======
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO transactions (
                    account_id, amount, location, event_time, is_fraud, fraud_probability,
                    user_transaction_count, user_avg_transaction_amount, deviation_from_user_avg,
                    transaction_hour, transaction_day_of_week, transaction_type, channel,
                    customer_age, customer_occupation, login_attempts, account_balance, user_primary_location, is_unusual_location
                )
                VALUES (%s, %s, %s, NOW(), NULL, NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    str(transaction.account_id),
                    float(transaction.TransactionAmount),
                    str(transaction.Location),
                    float(transaction.user_transaction_count),
                    float(transaction.user_avg_transaction_amount),
                    float(transaction.deviation_from_user_avg),
                    int(transaction.transaction_hour),
                    int(transaction.transaction_day_of_week),
                    str(transaction.TransactionType),
                    str(transaction.Channel),
                    int(transaction.CustomerAge),
                    str(transaction.CustomerOccupation),
                    int(transaction.LoginAttempts),
                    float(transaction.AccountBalance),
                    str(transaction.user_primary_location),
                    str(transaction.is_unusual_location)
                ),
            )
        conn.commit()
        return {"message": "Transaction ingested successfully", "data": transaction.model_dump()}
>>>>>>> 39e0989 (Initial commit: Add complete AI-powered real-time fraud detection system)
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

<<<<<<< HEAD
# API for model inference
=======
# API for model inference using Isolation Forest
>>>>>>> 39e0989 (Initial commit: Add complete AI-powered real-time fraud detection system)
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
<<<<<<< HEAD
=======
            transaction.user_transaction_count,
            transaction.user_avg_transaction_amount,
            transaction.deviation_from_user_avg,
            transaction.transaction_hour,
            transaction.transaction_day_of_week,
>>>>>>> 39e0989 (Initial commit: Add complete AI-powered real-time fraud detection system)
        ]).reshape(1, -1)

        categorical_features = encoder.transform([[
            transaction.TransactionType,
            transaction.Location,
            transaction.Channel,
            transaction.CustomerOccupation,
            transaction.user_primary_location,
<<<<<<< HEAD
        ]])

        # Combine numeric and categorical features
        features = np.hstack((numeric_features, categorical_features)).astype(np.float32)

        # Predict fraud probability using ONNX model
        input_name = onnx_session.get_inputs()[0].name
        output_name = onnx_session.get_outputs()[0].name
        fraud_probability = onnx_session.run([output_name], {input_name: features})[0][0][1]  # Probability of class 1
        is_fraud = fraud_probability >= 0.3  # Use the custom threshold of 0.3
=======
            transaction.is_unusual_location
        ]])

        features = np.hstack((numeric_features, categorical_features)).astype(np.float32)

        # Get anomaly score (the lower, the more anomalous)
        anomaly_score = float(-iso_forest.decision_function(features)[0])
        is_fraud = bool(iso_forest.predict(features)[0] == -1)  # <-- Cast to native bool
>>>>>>> 39e0989 (Initial commit: Add complete AI-powered real-time fraud detection system)

        # Save results to the database
        with conn.cursor() as cur:
            cur.execute(
                """
<<<<<<< HEAD
                INSERT INTO transactions (amount, location, event_time, is_fraud, fraud_probability)
                VALUES (%s, %s, NOW(), %s, %s)
                """,
                (transaction.TransactionAmount, transaction.Location, is_fraud, fraud_probability),
            )
        conn.commit()

        return {"fraud_probability": fraud_probability, "is_fraud": is_fraud}
=======
                INSERT INTO transactions (
                    account_id, amount, location, event_time, is_fraud, fraud_probability,
                    user_transaction_count, user_avg_transaction_amount, deviation_from_user_avg,
                    transaction_hour, transaction_day_of_week, transaction_type, channel,
                    customer_age, customer_occupation, login_attempts, account_balance, user_primary_location, is_unusual_location
                )
                VALUES (%s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    str(transaction.account_id),
                    float(transaction.TransactionAmount),
                    str(transaction.Location),
                    is_fraud,  # Now a native bool
                    anomaly_score,
                    float(transaction.user_transaction_count),
                    float(transaction.user_avg_transaction_amount),
                    float(transaction.deviation_from_user_avg),
                    int(transaction.transaction_hour),
                    int(transaction.transaction_day_of_week),
                    str(transaction.TransactionType),
                    str(transaction.Channel),
                    int(transaction.CustomerAge),
                    str(transaction.CustomerOccupation),
                    int(transaction.LoginAttempts),
                    float(transaction.AccountBalance),
                    str(transaction.user_primary_location),
                    str(transaction.is_unusual_location)
                ),
            )
        conn.commit()

        return {"anomaly_score": anomaly_score, "is_fraud": is_fraud}
>>>>>>> 39e0989 (Initial commit: Add complete AI-powered real-time fraud detection system)
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")