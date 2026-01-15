import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from mcp_server.tools import handle_delete_task
from models import User, Task
from sqlmodel import Session
import uuid
from datetime import datetime


@pytest.mark.asyncio
async def test_handle_delete_task_success():
    """Test successful task deletion"""
    # Mock user ID and task ID
    user_id = uuid.uuid4()
    task_id = uuid.uuid4()

    # Mock arguments for the tool
    arguments = {
        "task_id": str(task_id)
    }

    # Create mock task
    mock_task = Task(
        id=task_id,
        user_id=user_id,
        title="Task to Delete",
        description="Task Description",
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Mock database session
    mock_session = MagicMock(spec=Session)
    mock_session.exec = MagicMock(return_value=MagicMock())
    mock_session.exec.return_value.first.return_value = mock_task
    mock_session.delete = MagicMock()
    mock_session.commit = MagicMock()

    # Patch the get_session context manager
    with patch('mcp_server.tools.get_session') as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_session
        # Also mock the User query to return a user
        with patch('mcp_server.tools.User') as mock_user_class:
            mock_user = MagicMock()
            mock_get_session.return_value.__enter__.return_value.get.return_value = mock_user

            # Call the handler
            result = await handle_delete_task(arguments, user_id)

            # Verify the response
            assert len(result) == 1
            assert result[0].type == "text"
            assert "Successfully deleted task" in result[0].text
            assert "Task to Delete" in result[0].text


@pytest.mark.asyncio
async def test_handle_delete_task_not_found():
    """Test deleting a task that doesn't exist"""
    # Mock user ID and task ID
    user_id = uuid.uuid4()
    task_id = uuid.uuid4()

    # Mock arguments for the tool
    arguments = {
        "task_id": str(task_id)
    }

    # Mock database session - return None (task not found)
    mock_session = MagicMock(spec=Session)
    mock_session.exec = MagicMock(return_value=MagicMock())
    mock_session.exec.return_value.first.return_value = None

    # Patch the get_session context manager
    with patch('mcp_server.tools.get_session') as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_session
        # Also mock the User query to return a user
        with patch('mcp_server.tools.User') as mock_user_class:
            mock_user = MagicMock()
            mock_get_session.return_value.__enter__.return_value.get.return_value = mock_user

            # Call the handler
            result = await handle_delete_task(arguments, user_id)

            # Verify the error response
            assert len(result) == 1
            assert result[0].type == "text"
            assert "Error: Task not found or does not belong to this user" in result[0].text


@pytest.mark.asyncio
async def test_handle_delete_task_invalid_task_id():
    """Test deleting with an invalid task ID format"""
    # Mock user ID
    user_id = uuid.uuid4()

    # Mock arguments for the tool with invalid task_id
    arguments = {
        "task_id": "invalid-uuid-format"
    }

    # Call the handler
    result = await handle_delete_task(arguments, user_id)

    # Verify the error response
    assert len(result) == 1
    assert result[0].type == "text"
    assert "Error: Invalid task_id format" in result[0].text


@pytest.mark.asyncio
async def test_handle_delete_task_wrong_user():
    """Test deleting a task that belongs to a different user"""
    # Mock user ID and task ID
    user_id = uuid.uuid4()
    other_user_id = uuid.uuid4()
    task_id = uuid.uuid4()

    # Mock arguments for the tool
    arguments = {
        "task_id": str(task_id)
    }

    # Create mock task that belongs to a different user
    mock_task = Task(
        id=task_id,
        user_id=other_user_id,  # Different user
        title="Task to Delete",
        description="Task Description",
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Mock database session
    mock_session = MagicMock(spec=Session)
    mock_session.exec = MagicMock(return_value=MagicMock())
    mock_session.exec.return_value.first.return_value = mock_task

    # Patch the get_session context manager
    with patch('mcp_server.tools.get_session') as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_session
        # Also mock the User query to return a user
        with patch('mcp_server.tools.User') as mock_user_class:
            mock_user = MagicMock()
            mock_get_session.return_value.__enter__.return_value.get.return_value = mock_user

            # Call the handler
            result = await handle_delete_task(arguments, user_id)

            # Verify the error response
            assert len(result) == 1
            assert result[0].type == "text"
            assert "Error: Task not found or does not belong to this user" in result[0].text