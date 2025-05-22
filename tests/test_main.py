def test_ingest_transaction(client):
    transaction = {
        "TransactionAmount": 100.5,
        "CustomerAge": 30,
        "TransactionDuration": 5.0,
        "LoginAttempts": 1,
        "AccountBalance": 5000.0,
        "TransactionType": "Debit",
        "Location": "New York",
        "Channel": "Online",
        "CustomerOccupation": "Engineer",
        "user_primary_location": "New York"
    }
    response = client.post("/transactions/ingest", json=transaction)
    assert response.status_code == 200
    assert response.json()["message"] == "Transaction ingested successfully"

def test_score_transaction(client):
    transaction = {
        "TransactionAmount": 100.5,
        "CustomerAge": 30,
        "TransactionDuration": 5.0,
        "LoginAttempts": 1,
        "AccountBalance": 5000.0,
        "TransactionType": "Debit",
        "Location": "New York",
        "Channel": "Online",
        "CustomerOccupation": "Engineer",
        "user_primary_location": "New York"
    }
    response = client.post("/transactions/score", json=transaction)
    assert response.status_code == 200
    assert "fraud_probability" in response.json()
    assert "is_fraud" in response.json()