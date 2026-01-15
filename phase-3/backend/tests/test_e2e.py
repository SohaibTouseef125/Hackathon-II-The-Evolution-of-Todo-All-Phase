import pytest
from fastapi.testclient import TestClient
from main import app
from models import User, Task, Conversation, Message
from sqlmodel import Session, select
import uuid
from auth import create_access_token
from datetime import timedelta


def test_complete_conversation_flow():
    """Test a complete conversation flow: add task, list tasks, update task, complete task, delete task"""
    with TestClient(app) as client:
        # Create a mock user and token
        user_id = str(uuid.uuid4())
        token = create_access_token(data={"sub": user_id})

        # Step 1: Add a task through conversation
        response = client.post(
            f"/api/{user_id}/chat",
            json={"message": "Add a task to buy groceries"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        response_data = response.json()
        assert "conversation_id" in response_data
        assert "buy groceries" in response_data["response"].lower()
        conversation_id = response_data["conversation_id"]

        # Step 2: List tasks through conversation
        response = client.post(
            f"/api/{user_id}/chat",
            json={"message": "Show me my tasks", "conversation_id": conversation_id},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        response_data = response.json()
        assert "buy groceries" in response_data["response"].lower()

        # Step 3: Update the task through conversation
        response = client.post(
            f"/api/{user_id}/chat",
            json={"message": "Change the task 'buy groceries' to 'buy milk and eggs'", "conversation_id": conversation_id},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        response_data = response.json()
        assert "milk and eggs" in response_data["response"].lower()

        # Step 4: Complete the task through conversation
        response = client.post(
            f"/api/{user_id}/chat",
            json={"message": "Mark the task 'buy milk and eggs' as completed", "conversation_id": conversation_id},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        response_data = response.json()
        assert "completed" in response_data["response"].lower()

        # Step 5: Delete the task through conversation
        response = client.post(
            f"/api/{user_id}/chat",
            json={"message": "Delete the task 'buy milk and eggs'", "conversation_id": conversation_id},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        response_data = response.json()
        assert "deleted" in response_data["response"].lower()


def test_conversation_history_preservation():
    """Test that conversation history is preserved between requests"""
    with TestClient(app) as client:
        # Create a mock user and token
        user_id = str(uuid.uuid4())
        token = create_access_token(data={"sub": user_id})

        # Start a conversation
        response = client.post(
            f"/api/{user_id}/chat",
            json={"message": "Add a task to call mom"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        response_data = response.json()
        assert "conversation_id" in response_data
        conversation_id = response_data["conversation_id"]

        # Continue the conversation with context
        response = client.post(
            f"/api/{user_id}/chat",
            json={"message": "What was the last task I asked you to add?", "conversation_id": conversation_id},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        response_data = response.json()
        # The AI should have context about the previous conversation
        # This is more about testing that the conversation_id is properly handled


def test_multiple_users_isolation():
    """Test that users cannot access each other's conversations or tasks"""
    with TestClient(app) as client:
        # Create two different users
        user1_id = str(uuid.uuid4())
        user2_id = str(uuid.uuid4())

        token1 = create_access_token(data={"sub": user1_id})
        token2 = create_access_token(data={"sub": user2_id})

        # User 1 creates a task
        response = client.post(
            f"/api/{user1_id}/chat",
            json={"message": "Add a task to buy groceries"},
            headers={"Authorization": f"Bearer {token1}"}
        )

        assert response.status_code == 200
        user1_conversation_id = response.json()["conversation_id"]

        # User 2 tries to access User 1's conversation (should fail)
        response = client.post(
            f"/api/{user1_id}/chat",  # Trying to access user1's endpoint
            json={"message": "What tasks do I have?", "conversation_id": user1_conversation_id},
            headers={"Authorization": f"Bearer {token2}"}  # Using user2's token
        )

        # Should return 403 Forbidden because user2 is trying to access user1's data
        assert response.status_code == 403


def test_invalid_conversation_id():
    """Test handling of invalid conversation IDs"""
    with TestClient(app) as client:
        # Create a mock user and token
        user_id = str(uuid.uuid4())
        token = create_access_token(data={"sub": user_id})

        # Try to use an invalid conversation ID
        invalid_conversation_id = "invalid-uuid-format"

        response = client.post(
            f"/api/{user_id}/chat",
            json={"message": "Add a task to buy groceries", "conversation_id": invalid_conversation_id},
            headers={"Authorization": f"Bearer {token}"}
        )

        # Should return 422 Unprocessable Entity due to invalid UUID format
        assert response.status_code == 422


def test_empty_message_handling():
    """Test handling of empty or invalid messages"""
    with TestClient(app) as client:
        # Create a mock user and token
        user_id = str(uuid.uuid4())
        token = create_access_token(data={"sub": user_id})

        # Try to send an empty message
        response = client.post(
            f"/api/{user_id}/chat",
            json={"message": ""},
            headers={"Authorization": f"Bearer {token}"}
        )

        # Should return 422 Unprocessable Entity due to empty message
        assert response.status_code == 422

        # Try to send a non-string message
        response = client.post(
            f"/api/{user_id}/chat",
            json={"message": 123},
            headers={"Authorization": f"Bearer {token}"}
        )

        # Should return 422 Unprocessable Entity due to non-string message
        assert response.status_code == 422