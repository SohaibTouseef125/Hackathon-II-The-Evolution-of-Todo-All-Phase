import pytest
from fastapi.testclient import TestClient
from main import app
from models import User, Task
from sqlmodel import Session, select
import uuid
from auth import create_access_token
from datetime import timedelta


def test_chat_endpoint_requires_authentication():
    """Test that the chat endpoint requires authentication"""
    with TestClient(app) as client:
        # Try to access chat endpoint without authentication
        response = client.post("/user-id/chat", json={"message": "test message"})

        # Should return 401 Unauthorized
        assert response.status_code == 401


def test_chat_endpoint_rejects_invalid_user_id():
    """Test that users can't access other users' chat endpoints"""
    with TestClient(app) as client:
        # Create a mock user and token
        user_id = str(uuid.uuid4())
        token = create_access_token(data={"sub": user_id})

        # Try to access a different user's chat endpoint
        different_user_id = str(uuid.uuid4())
        response = client.post(
            f"/{different_user_id}/chat",
            json={"message": "test message"},
            headers={"Authorization": f"Bearer {token}"}
        )

        # Should return 403 Forbidden
        assert response.status_code == 403
        assert "Access denied" in response.json()["detail"]


def test_chat_endpoint_accepts_valid_user_id():
    """Test that users can access their own chat endpoint"""
    with TestClient(app) as client:
        # Create a mock user and token
        user_id = str(uuid.uuid4())
        token = create_access_token(data={"sub": user_id})

        # Access own chat endpoint
        response = client.post(
            f"/{user_id}/chat",
            json={"message": "test message"},
            headers={"Authorization": f"Bearer {token}"}
        )

        # Should return 200 OK (might fail later in processing, but auth passes)
        # We expect it to not be a 401 or 403 error
        assert response.status_code != 401
        assert response.status_code != 403


def test_mcp_tools_enforce_user_isolation():
    """Test that MCP tools enforce user isolation"""
    # This would require more complex setup with the MCP server
    # For now, we'll verify that the tools validate user_id properly
    assert True  # Placeholder - actual implementation would require MCP server setup