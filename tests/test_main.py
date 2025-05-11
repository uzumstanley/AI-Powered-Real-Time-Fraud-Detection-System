import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta, timezone
import jwt

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Mock Redis client
app.state.redis_client = None

# Generate a test JWT token
def create_test_token():
    payload = {
        "sub": "test_user",
        "exp": datetime.now(timezone.utc) + timedelta(hours=2)  # Use timezone-aware datetime
    }
    return jwt.encode(payload, os.getenv("JWT_SECRET", "your_default_secret"), algorithm="HS256")

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

def test_score_transaction(client):
    # Mock transaction data with 204 features
    transaction = {
        "id": "txn_123",
        "account": "acc_456",
        "features": [0.1] * 204,  # Create a list with 204 elements
        "time": "2025-05-10T12:00:00"
    }
    # Generate a valid JWT token
    token = create_test_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/transactions/score", json=transaction, headers=headers)
    assert response.status_code == 200
    assert "score" in response.json()
    assert "is_fraud" in response.json()