import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from mcp_server.tools import handle_add_task
from models import User, Task
from sqlmodel import Session, select
import uuid
from datetime import datetime


@pytest.mark.asyncio
async def test_handle_add_task_success():
    """Test successful task creation via add_task handler"""
    # Mock user ID
    user_id = uuid.uuid4()

    # Mock arguments for the tool
    arguments = {
        "title": "Test Task",
        "description": "Test Description"
    }

    # Mock database session
    mock_session = MagicMock(spec=Session)
    mock_session.add = MagicMock()
    mock_session.commit = MagicMock()
    mock_session.refresh = MagicMock()

    # Mock task object that will be created
    mock_task = Task(
        id=uuid.uuid4(),
        user_id=user_id,
        title="Test Task",
        description="Test Description",
        completed=False
    )
    mock_session.refresh.side_effect = lambda obj: setattr(obj, 'id', mock_task.id)

    # Patch the get_session context manager
    with patch('mcp_server.tools.get_session') as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_session
        # Also mock the User query to return a user
        with patch('mcp_server.tools.User') as mock_user_class:
            mock_user = MagicMock()
            mock_get_session.return_value.__enter__.return_value.get.return_value = mock_user

            # Call the handler
            result = await handle_add_task(arguments, user_id)

            # Verify the response
            assert len(result) == 1
            assert result[0].type == "text"
            assert "Successfully created task" in result[0].text
            assert "Test Task" in result[0].text


@pytest.mark.asyncio
async def test_handle_add_task_missing_title():
    """Test add_task handler with missing title"""
    # Mock user ID
    user_id = uuid.uuid4()

    # Mock arguments without title
    arguments = {
        "description": "Test Description"
    }

    # Call the handler
    result = await handle_add_task(arguments, user_id)

    # Verify the error response
    assert len(result) == 1
    assert result[0].type == "text"
    assert "Error: Title must be 1-200 characters" in result[0].text


@pytest.mark.asyncio
async def test_handle_add_task_empty_title():
    """Test add_task handler with empty title"""
    # Mock user ID
    user_id = uuid.uuid4()

    # Mock arguments with empty title
    arguments = {
        "title": "",
        "description": "Test Description"
    }

    # Call the handler
    result = await handle_add_task(arguments, user_id)

    # Verify the error response
    assert len(result) == 1
    assert result[0].type == "text"
    assert "Error: Title must be 1-200 characters" in result[0].text


@pytest.mark.asyncio
async def test_handle_add_task_long_title():
    """Test add_task handler with title that's too long"""
    # Mock user ID
    user_id = uuid.uuid4()

    # Mock arguments with very long title
    arguments = {
        "title": "A" * 201,  # Exceeds 200 character limit
        "description": "Test Description"
    }

    # Call the handler
    result = await handle_add_task(arguments, user_id)

    # Verify the error response
    assert len(result) == 1
    assert result[0].type == "text"
    assert "Error: Title must be 1-200 characters" in result[0].text