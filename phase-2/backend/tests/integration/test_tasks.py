import pytest
from fastapi.testclient import TestClient
from main import app
from db import get_session, engine
from models import User, Task
from sqlmodel import Session, SQLModel
from unittest.mock import patch
import uuid


@pytest.fixture(name="client")
def client_fixture():
    def get_test_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_task_crud_operations(client: TestClient):
    """Test task CRUD operations"""
    # First register and login a user to get a token
    register_response = client.post("/api/auth/register", json={
        "email": "taskuser@example.com",
        "name": "Task User",
        "password": "securepassword"
    })
    assert register_response.status_code == 200

    login_response = client.post("/api/auth/login", data={
        "email": "taskuser@example.com",
        "password": "securepassword"
    })
    assert login_response.status_code == 200
    token_data = login_response.json()
    access_token = token_data["access_token"]

    # Set up headers with the access token
    headers = {"Authorization": f"Bearer {access_token}"}

    # Test creating a task
    create_response = client.post("/api/tasks", json={
        "title": "Test Task",
        "description": "Test Description",
        "completed": False
    }, headers=headers)
    assert create_response.status_code == 200
    created_task = create_response.json()
    assert created_task["title"] == "Test Task"
    assert created_task["description"] == "Test Description"
    task_id = created_task["id"]

    # Test getting all tasks
    get_all_response = client.get("/api/tasks", headers=headers)
    assert get_all_response.status_code == 200
    tasks = get_all_response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Test Task"

    # Test getting a specific task
    get_one_response = client.get(f"/api/tasks/{task_id}", headers=headers)
    assert get_one_response.status_code == 200
    task = get_one_response.json()
    assert task["title"] == "Test Task"

    # Test updating a task
    update_response = client.put(f"/api/tasks/{task_id}", json={
        "title": "Updated Task",
        "description": "Updated Description"
    }, headers=headers)
    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["title"] == "Updated Task"

    # Test toggling task completion
    toggle_response = client.patch(f"/api/tasks/{task_id}/complete", headers=headers)
    assert toggle_response.status_code == 200
    toggled_task = toggle_response.json()
    assert toggled_task["completed"] == True

    # Test deleting a task
    delete_response = client.delete(f"/api/tasks/{task_id}", headers=headers)
    assert delete_response.status_code == 200

    # Verify the task is deleted
    get_after_delete_response = client.get(f"/api/tasks/{task_id}", headers=headers)
    assert get_after_delete_response.status_code == 404


def test_user_data_isolation(client: TestClient):
    """Test that users can only access their own tasks"""
    # Register first user
    user1_response = client.post("/api/auth/register", json={
        "email": "user1@example.com",
        "name": "User 1",
        "password": "securepassword"
    })
    assert user1_response.status_code == 200

    # Register second user
    user2_response = client.post("/api/auth/register", json={
        "email": "user2@example.com",
        "name": "User 2",
        "password": "securepassword"
    })
    assert user2_response.status_code == 200

    # Login as first user
    login1_response = client.post("/api/auth/login", data={
        "email": "user1@example.com",
        "password": "securepassword"
    })
    assert login1_response.status_code == 200
    token1 = login1_response.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}

    # Login as second user
    login2_response = client.post("/api/auth/login", data={
        "email": "user2@example.com",
        "password": "securepassword"
    })
    assert login2_response.status_code == 200
    token2 = login2_response.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    # First user creates a task
    create_task_response = client.post("/api/tasks", json={
        "title": "User 1 Task",
        "description": "Task for User 1",
        "completed": False
    }, headers=headers1)
    assert create_task_response.status_code == 200
    task_data = create_task_response.json()
    task_id = task_data["id"]
    assert task_data["title"] == "User 1 Task"

    # First user should see their task
    get_tasks1_response = client.get("/api/tasks", headers=headers1)
    assert get_tasks1_response.status_code == 200
    user1_tasks = get_tasks1_response.json()
    assert len(user1_tasks) == 1

    # Second user should not see first user's task
    get_tasks2_response = client.get("/api/tasks", headers=headers2)
    assert get_tasks2_response.status_code == 200
    user2_tasks = get_tasks2_response.json()
    assert len(user2_tasks) == 0

    # Second user should not be able to access first user's task directly
    get_task2_response = client.get(f"/api/tasks/{task_id}", headers=headers2)
    assert get_task2_response.status_code == 404


if __name__ == "__main__":
    # Run the tests if this file is executed directly
    print("Running task integration tests...")
    print("✓ test_task_crud_operations defined")
    print("✓ test_user_data_isolation defined")
    print("All task integration tests defined!")