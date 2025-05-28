import jwt
from datetime import datetime, timedelta

# Load the secret from your .env file
secret = "da26ee4395ddf17721ff931a45f997fe7f5d729f4292cda1b3848ff6c0eb8e8a"  # Replace with your JWT_SECRET

# Define the payload
payload = {
    "sub": "test_user",  # Subject (user identifier)
    "exp": datetime.utcnow() + timedelta(hours=2),  # Expiration time (2 hours from now)
}

# Generate the token
token = jwt.encode(payload, secret, algorithm="HS256")
print("Generated JWT Token:", token)