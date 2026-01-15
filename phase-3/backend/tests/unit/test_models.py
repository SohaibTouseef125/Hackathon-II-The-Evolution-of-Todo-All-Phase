import pytest
from sqlmodel import Session, select
from datetime import datetime
import uuid
from models import User, Task, UserCreate, TaskCreate


def test_user_model():
    """Test User model creation"""
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "hashed_password": "hashed_password"
    }
    user = User(**user_data)

    assert user.email == "test@example.com"
    assert user.name == "Test User"
    assert user.hashed_password == "hashed_password"
    assert user.is_active == True
    assert isinstance(user.id, uuid.UUID)
    assert isinstance(user.created_at, datetime)


def test_task_model():
    """Test Task model creation"""
    user_id = uuid.uuid4()
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "completed": False,
        "user_id": user_id
    }
    task = Task(**task_data)

    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed == False
    assert task.user_id == user_id
    assert isinstance(task.id, uuid.UUID)
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


def test_user_create_model():
    """Test UserCreate model validation"""
    user_create = UserCreate(
        email="test@example.com",
        name="Test User",
        password="securepassword"
    )

    assert user_create.email == "test@example.com"
    assert user_create.name == "Test User"
    assert user_create.password == "securepassword"


def test_task_create_model():
    """Test TaskCreate model validation"""
    task_create = TaskCreate(
        title="Test Task",
        description="Test Description",
        completed=False
    )

    assert task_create.title == "Test Task"
    assert task_create.description == "Test Description"
    assert task_create.completed == False


if __name__ == "__main__":
    test_user_model()
    test_task_model()
    test_user_create_model()
    test_task_create_model()
    print("All model tests passed!")