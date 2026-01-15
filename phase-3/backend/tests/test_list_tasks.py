import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from mcp_server.tools import handle_list_tasks
from models import User, Task
from sqlmodel import Session, select
import uuid
from datetime import datetime


@pytest.mark.asyncio
async def test_handle_list_tasks_all_success():
    """Test successful listing of all tasks"""
    # Mock user ID
    user_id = uuid.uuid4()

    # Mock arguments for the tool
    arguments = {
        "status": "all"
    }

    # Create mock tasks
    mock_tasks = [
        Task(
            id=uuid.uuid4(),
            user_id=user_id,
            title="Task 1",
            description="Description 1",
            completed=False,
            created_at=datetime.utcnow()
        ),
        Task(
            id=uuid.uuid4(),
            user_id=user_id,
            title="Task 2",
            description="Description 2",
            completed=True,
            created_at=datetime.utcnow()
        )
    ]

    # Mock database session
    mock_session = MagicMock(spec=Session)
    mock_session.exec = MagicMock(return_value=MagicMock())
    mock_session.exec.return_value.all.return_value = mock_tasks

    # Patch the get_session context manager
    with patch('mcp_server.tools.get_session') as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_session
        # Also mock the User query to return a user
        with patch('mcp_server.tools.User') as mock_user_class:
            mock_user = MagicMock()
            mock_get_session.return_value.__enter__.return_value.get.return_value = mock_user

            # Call the handler
            result = await handle_list_tasks(arguments, user_id)

            # Verify the response
            assert len(result) == 1
            assert result[0].type == "text"
            assert "Found 2 all tasks" in result[0].text
            assert "Task 1" in result[0].text
            assert "Task 2" in result[0].text


@pytest.mark.asyncio
async def test_handle_list_tasks_pending_success():
    """Test successful listing of pending tasks"""
    # Mock user ID
    user_id = uuid.uuid4()

    # Mock arguments for the tool
    arguments = {
        "status": "pending"
    }

    # Create mock tasks (only one pending)
    mock_tasks = [
        Task(
            id=uuid.uuid4(),
            user_id=user_id,
            title="Pending Task",
            description="Description",
            completed=False,
            created_at=datetime.utcnow()
        )
    ]

    # Mock database session
    mock_session = MagicMock(spec=Session)
    mock_session.exec = MagicMock(return_value=MagicMock())
    mock_session.exec.return_value.all.return_value = mock_tasks

    # Patch the get_session context manager
    with patch('mcp_server.tools.get_session') as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_session
        # Also mock the User query to return a user
        with patch('mcp_server.tools.User') as mock_user_class:
            mock_user = MagicMock()
            mock_get_session.return_value.__enter__.return_value.get.return_value = mock_user

            # Call the handler
            result = await handle_list_tasks(arguments, user_id)

            # Verify the response
            assert len(result) == 1
            assert result[0].type == "text"
            assert "Found 1 pending tasks" in result[0].text
            assert "Pending Task" in result[0].text


@pytest.mark.asyncio
async def test_handle_list_tasks_completed_success():
    """Test successful listing of completed tasks"""
    # Mock user ID
    user_id = uuid.uuid4()

    # Mock arguments for the tool
    arguments = {
        "status": "completed"
    }

    # Create mock tasks (only one completed)
    mock_tasks = [
        Task(
            id=uuid.uuid4(),
            user_id=user_id,
            title="Completed Task",
            description="Description",
            completed=True,
            created_at=datetime.utcnow()
        )
    ]

    # Mock database session
    mock_session = MagicMock(spec=Session)
    mock_session.exec = MagicMock(return_value=MagicMock())
    mock_session.exec.return_value.all.return_value = mock_tasks

    # Patch the get_session context manager
    with patch('mcp_server.tools.get_session') as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_session
        # Also mock the User query to return a user
        with patch('mcp_server.tools.User') as mock_user_class:
            mock_user = MagicMock()
            mock_get_session.return_value.__enter__.return_value.get.return_value = mock_user

            # Call the handler
            result = await handle_list_tasks(arguments, user_id)

            # Verify the response
            assert len(result) == 1
            assert result[0].type == "text"
            assert "Found 1 completed tasks" in result[0].text
            assert "Completed Task" in result[0].text


@pytest.mark.asyncio
async def test_handle_list_tasks_no_tasks():
    """Test listing tasks when no tasks exist"""
    # Mock user ID
    user_id = uuid.uuid4()

    # Mock arguments for the tool
    arguments = {
        "status": "all"
    }

    # Create empty mock tasks list
    mock_tasks = []

    # Mock database session
    mock_session = MagicMock(spec=Session)
    mock_session.exec = MagicMock(return_value=MagicMock())
    mock_session.exec.return_value.all.return_value = mock_tasks

    # Patch the get_session context manager
    with patch('mcp_server.tools.get_session') as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_session
        # Also mock the User query to return a user
        with patch('mcp_server.tools.User') as mock_user_class:
            mock_user = MagicMock()
            mock_get_session.return_value.__enter__.return_value.get.return_value = mock_user

            # Call the handler
            result = await handle_list_tasks(arguments, user_id)

            # Verify the response
            assert len(result) == 1
            assert result[0].type == "text"
            assert "No tasks found for this user" in result[0].text