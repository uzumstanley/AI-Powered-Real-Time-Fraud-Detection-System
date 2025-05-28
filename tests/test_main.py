<<<<<<< HEAD
def test_ingest_transaction(client):
    transaction = {
=======
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ingest_transaction():
    transaction = {
        "account_id": "test_account",
>>>>>>> 39e0989 (Initial commit: Add complete AI-powered real-time fraud detection system)
        "TransactionAmount": 100.5,
        "CustomerAge": 30,
        "TransactionDuration": 5.0,
        "LoginAttempts": 1,
        "AccountBalance": 5000.0,
<<<<<<< HEAD
=======
        "user_transaction_count": 10,
        "user_avg_transaction_amount": 200.0,
        "deviation_from_user_avg": 0.0,
        "transaction_hour": 14,
        "transaction_day_of_week": 2,
>>>>>>> 39e0989 (Initial commit: Add complete AI-powered real-time fraud detection system)
        "TransactionType": "Debit",
        "Location": "New York",
        "Channel": "Online",
        "CustomerOccupation": "Engineer",
<<<<<<< HEAD
        "user_primary_location": "New York"
    }
    response = client.post("/transactions/ingest", json=transaction)
    assert response.status_code == 200
    assert response.json()["message"] == "Transaction ingested successfully"

def test_score_transaction(client):
    transaction = {
=======
        "user_primary_location": "New York",
        "is_unusual_location": "False"
    }
    response = client.post("/transactions/ingest", json=transaction)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["message"] == "Transaction ingested successfully"

def test_score_transaction():
    transaction = {
        "account_id": "test_account",
>>>>>>> 39e0989 (Initial commit: Add complete AI-powered real-time fraud detection system)
        "TransactionAmount": 100.5,
        "CustomerAge": 30,
        "TransactionDuration": 5.0,
        "LoginAttempts": 1,
        "AccountBalance": 5000.0,
<<<<<<< HEAD
=======
        "user_transaction_count": 10,
        "user_avg_transaction_amount": 200.0,
        "deviation_from_user_avg": 0.0,
        "transaction_hour": 14,
        "transaction_day_of_week": 2,
>>>>>>> 39e0989 (Initial commit: Add complete AI-powered real-time fraud detection system)
        "TransactionType": "Debit",
        "Location": "New York",
        "Channel": "Online",
        "CustomerOccupation": "Engineer",
<<<<<<< HEAD
        "user_primary_location": "New York"
    }
    response = client.post("/transactions/score", json=transaction)
    assert response.status_code == 200
    assert "fraud_probability" in response.json()
=======
        "user_primary_location": "New York",
        "is_unusual_location": "False"
    }
    response = client.post("/transactions/score", json=transaction)
    print(response.json())
    assert response.status_code == 200
    assert "anomaly_score" in response.json()
>>>>>>> 39e0989 (Initial commit: Add complete AI-powered real-time fraud detection system)
    assert "is_fraud" in response.json()