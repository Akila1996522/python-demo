import sys
import os
import pytest
import jwt
import datetime
from fastapi.testclient import TestClient
from app.main import app
from app.services.jwt_service import decode_jwt, decode_refresh_token

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

client = TestClient(app)

# Secret and algorithm must match your actual app settings
JWT_SECRET = "your_jwt_secret_key"
JWT_ALGORITHM = "HS256"

def generate_expired_token():
    """Generate a JWT that is already expired."""
    return jwt.encode({
        "email": "test@example.com",
        "password": "dummy",
        "imap_server": "imap.example.com",
        "smtp_server": "smtp.example.com",
        "imap_port": 993,
        "smtp_port": 587,
        "exp": int((datetime.datetime.utcnow() - datetime.timedelta(seconds=10)).timestamp())
    }, JWT_SECRET, algorithm=JWT_ALGORITHM)

def test_validate_mailbox():
    response = client.post(
        "/api/v1/auth/validate",
        json={"mailbox_email": "test@example.com"},
        headers={"Authorization": "Bearer dummy_token"}  # Adjust as needed
    )
    assert response.status_code in [200, 400, 401]

def test_fetch_emails():
    response = client.get(
        "/api/v1/mailbox/emails?mailbox_email=test@example.com",
        headers={"Authorization": "Bearer dummy_token"}
    )
    assert response.status_code in [200, 400, 401]

def test_jwt_token_expiry():
    expired_token = generate_expired_token()
    with pytest.raises(Exception) as exc_info:
        decode_jwt(expired_token)
    assert str(exc_info.value) == "Token has expired"

def test_refresh_token_expiry():
    expired_token = generate_expired_token()
    with pytest.raises(Exception) as exc_info:
        decode_refresh_token(expired_token)
    assert str(exc_info.value) == "Refresh token has expired"
