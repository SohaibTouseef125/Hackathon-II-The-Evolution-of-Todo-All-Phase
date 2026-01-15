import pytest
from fastapi.testclient import TestClient
from main import app
from auth import create_access_token
import uuid


def test_unauthenticated_request():
    """Test that unauthenticated requests are rejected"""
    with TestClient(app) as client:
        # Try to access the chat endpoint without authentication
        user_id = str(uuid.uuid4())
        response = client.post(
            f"/api/{user_id}/chat",
            json={"message": "Test message"}
        )

        # Should return 401 Unauthorized
        assert response.status_code == 401


def test_invalid_token():
    """Test that requests with invalid tokens are rejected"""
    with TestClient(app) as client:
        # Try to access the chat endpoint with an invalid token
        user_id = str(uuid.uuid4())
        response = client.post(
            f"/api/{user_id}/chat",
            json={"message": "Test message"},
            headers={"Authorization": "Bearer invalid-token"}
        )

        # Should return 401 Unauthorized
        assert response.status_code == 401


def test_cross_user_access_denied():
    """Test that users cannot access other users' chat endpoints"""
    with TestClient(app) as client:
        # Create tokens for two different users
        user1_id = str(uuid.uuid4())
        user2_id = str(uuid.uuid4())

        token1 = create_access_token(data={"sub": user1_id})
        token2 = create_access_token(data={"sub": user2_id})

        # User 1 tries to access User 2's chat endpoint
        response = client.post(
            f"/api/{user2_id}/chat",  # Endpoint for user2
            json={"message": "Test message"},
            headers={"Authorization": f"Bearer {token1}"}  # Token for user1
        )

        # Should return 403 Forbidden
        assert response.status_code == 403
        assert "Access denied" in response.json()["detail"]

        # User 2 tries to access User 1's chat endpoint
        response = client.post(
            f"/api/{user1_id}/chat",  # Endpoint for user1
            json={"message": "Test message"},
            headers={"Authorization": f"Bearer {token2}"}  # Token for user2
        )

        # Should return 403 Forbidden
        assert response.status_code == 403
        assert "Access denied" in response.json()["detail"]


def test_same_user_access_allowed():
    """Test that users can access their own chat endpoints"""
    with TestClient(app) as client:
        # Create a user and token
        user_id = str(uuid.uuid4())
        token = create_access_token(data={"sub": user_id})

        # User accesses their own chat endpoint
        response = client.post(
            f"/api/{user_id}/chat",  # Endpoint for the same user
            json={"message": "Add a task to buy groceries"},
            headers={"Authorization": f"Bearer {token}"}
        )

        # Should return 200 OK (or possibly 422 if there are other validation issues, but not 403)
        assert response.status_code in [200, 422]  # 422 is acceptable if there are other validation errors


def test_token_payload_validation():
    """Test that tokens with invalid payloads are rejected"""
    with TestClient(app) as client:
        # Create a token with an invalid payload structure
        user_id = str(uuid.uuid4())

        # Manually create a token with an invalid subject format
        # For this test, we'll rely on the fact that our auth system expects a valid UUID in the subject
        token_with_invalid_user = create_access_token(data={"sub": "not-a-valid-uuid"})

        response = client.post(
            f"/api/{user_id}/chat",
            json={"message": "Test message"},
            headers={"Authorization": f"Bearer {token_with_invalid_user}"}
        )

        # Depending on implementation, this might fail during token validation or user lookup
        # At minimum, it should not succeed with a 200
        assert response.status_code in [401, 403, 422]


def test_expired_token():
    """Test that expired tokens are rejected"""
    with TestClient(app) as client:
        # Create an expired token
        user_id = str(uuid.uuid4())
        # Create a token that expired in the past
        from datetime import datetime, timedelta
        from jose import JWTError, jwt
        import os

        secret_key = os.getenv("SECRET_KEY", "dev-secret-key")
        expire = datetime.utcnow() - timedelta(minutes=15)  # Expired 15 minutes ago
        to_encode = {"sub": str(user_id), "exp": expire.timestamp()}
        expired_token = jwt.encode(to_encode, secret_key, algorithm="HS256")

        response = client.post(
            f"/api/{user_id}/chat",
            json={"message": "Test message"},
            headers={"Authorization": f"Bearer {expired_token}"}
        )

        # Should return 401 Unauthorized due to expired token
        assert response.status_code == 401


def test_user_id_format_validation():
    """Test that invalid user ID formats in the URL are handled properly"""
    with TestClient(app) as client:
        # Create a valid token
        user_id = str(uuid.uuid4())
        token = create_access_token(data={"sub": user_id})

        # Try to access with an invalid user ID format in the URL
        response = client.post(
            f"/api/invalid-user-id-format/chat",  # Invalid user ID format
            json={"message": "Test message"},
            headers={"Authorization": f"Bearer {token}"}
        )

        # Should return 422 Unprocessable Entity or 404 Not Found depending on FastAPI's validation
        assert response.status_code in [422, 404, 403]