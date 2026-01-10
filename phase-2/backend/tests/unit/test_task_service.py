import pytest
from unittest.mock import Mock, MagicMock
from sqlmodel import Session, select
from datetime import datetime
import uuid
from models import Task, TaskCreate
from services.task_service import TaskService


def test_create_task():
    """Test creating a task using TaskService"""
    # Mock session
    mock_session = Mock(spec=Session)

    # Create test data
    task_create = TaskCreate(
        title="Test Task",
        description="Test Description",
        completed=False
    )
    user_id = uuid.uuid4()

    # Call the service method
    result = TaskService.create_task(mock_session, task_create, user_id)

    # Assertions
    assert result.title == task_create.title
    assert result.description == task_create.description
    assert result.completed == task_create.completed
    assert result.user_id == user_id
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_get_tasks_by_user():
    """Test getting tasks by user using TaskService"""
    # Mock session
    mock_session = Mock(spec=Session)
    mock_session.exec.return_value.all.return_value = []

    # Create test data
    user_id = uuid.uuid4()

    # Call the service method
    result = TaskService.get_tasks_by_user(mock_session, user_id)

    # Assertions
    assert result == []
    mock_session.exec.assert_called_once()


def test_get_task_by_id():
    """Test getting a specific task by ID using TaskService"""
    # Mock session
    mock_session = Mock(spec=Session)
    mock_session.exec.return_value.first.return_value = None

    # Create test data
    task_id = uuid.uuid4()
    user_id = uuid.uuid4()

    # Call the service method
    result = TaskService.get_task_by_id(mock_session, task_id, user_id)

    # Assertions
    assert result is None
    mock_session.exec.assert_called_once()


def test_update_task():
    """Test updating a task using TaskService"""
    # Mock session
    mock_session = Mock(spec=Session)

    # Create test data
    original_task = Task(
        id=uuid.uuid4(),
        title="Original Task",
        description="Original Description",
        completed=False,
        user_id=uuid.uuid4()
    )

    task_update = Mock()
    task_update.dict.return_value = {"title": "Updated Task"}
    # Simulate the exclude_unset=True behavior by returning only the fields that are set
    def mock_dict(exclude_unset=False):
        if exclude_unset:
            # In real Pydantic, exclude_unset=True excludes fields not explicitly set
            # For this mock, just return the fields that were set
            return {"title": "Updated Task"}
        return {"title": "Updated Task"}

    task_update.dict = mock_dict

    # Call the service method
    result = TaskService.update_task(mock_session, original_task, task_update)

    # Assertions
    assert result.title == "Updated Task"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_delete_task():
    """Test deleting a task using TaskService"""
    # Mock session
    mock_session = Mock(spec=Session)

    # Create test data
    task = Task(
        id=uuid.uuid4(),
        title="Test Task",
        description="Test Description",
        completed=False,
        user_id=uuid.uuid4()
    )

    # Call the service method
    result = TaskService.delete_task(mock_session, task)

    # Assertions
    assert result is True
    mock_session.delete.assert_called_once()
    mock_session.commit.assert_called_once()


def test_toggle_task_completion():
    """Test toggling task completion using TaskService"""
    # Mock session
    mock_session = Mock(spec=Session)

    # Create test data
    task = Task(
        id=uuid.uuid4(),
        title="Test Task",
        description="Test Description",
        completed=False,
        user_id=uuid.uuid4()
    )

    # Call the service method
    result = TaskService.toggle_task_completion(mock_session, task)

    # Assertions
    assert result.completed == True  # Toggled from False to True
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


if __name__ == "__main__":
    test_create_task()
    test_get_tasks_by_user()
    test_get_task_by_id()
    test_update_task()
    test_delete_task()
    test_toggle_task_completion()
    print("All task service tests passed!")