import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from agents.chat_agent import ChatAgent
from mcp.client.stdio import stdio_client
import json


@pytest.mark.asyncio
async def test_agent_processes_message_and_calls_tool():
    """Test that the agent processes a message and correctly calls MCP tools"""
    # Create a ChatAgent instance
    agent = ChatAgent()

    # Mock the stdio_client context manager
    with patch('agents.chat_agent.stdio_client') as mock_stdio_client:
        # Create a mock client
        mock_client = AsyncMock()
        mock_stdio_client.return_value.__aenter__.return_value = mock_client

        # Mock the call_tool response for add_task
        mock_result = MagicMock()
        mock_result.text = "Successfully created task 'Buy groceries' with ID: 123e4567-e89b-12d3-a456-426614174000"
        mock_client.call_tool.return_value = [mock_result]

        # Process a message that should trigger the add_task tool
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        message = "Add a task to buy groceries"

        result = await agent.process_message(user_id, message)

        # Verify that the result contains the expected response
        assert "response" in result
        assert "tool_calls" in result
        assert len(result["tool_calls"]) > 0

        # Verify that the add_task tool was called
        assert result["tool_calls"][0]["name"] == "add_task"
        assert "buy groceries" in json.loads(result["tool_calls"][0]["arguments"])["title"]

        # Verify that the MCP client was called
        mock_client.call_tool.assert_called_once()


@pytest.mark.asyncio
async def test_agent_processes_list_tasks():
    """Test that the agent processes a message to list tasks"""
    # Create a ChatAgent instance
    agent = ChatAgent()

    # Mock the stdio_client context manager
    with patch('agents.chat_agent.stdio_client') as mock_stdio_client:
        # Create a mock client
        mock_client = AsyncMock()
        mock_stdio_client.return_value.__aenter__.return_value = mock_client

        # Mock the call_tool response for list_tasks
        mock_result = MagicMock()
        mock_result.text = "Found 2 pending tasks:\n- 123e4567-e89b-12d3-a456-426614174001: Buy groceries (pending)\n- 123e4567-e89b-12d3-a456-426614174002: Call mom (pending)"
        mock_client.call_tool.return_value = [mock_result]

        # Process a message that should trigger the list_tasks tool
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        message = "Show me my pending tasks"

        result = await agent.process_message(user_id, message)

        # Verify that the result contains the expected response
        assert "response" in result
        assert "tool_calls" in result
        assert len(result["tool_calls"]) > 0

        # Verify that the list_tasks tool was called
        assert result["tool_calls"][0]["name"] == "list_tasks"

        # Verify that the MCP client was called
        mock_client.call_tool.assert_called_once()


@pytest.mark.asyncio
async def test_agent_handles_conversation_history():
    """Test that the agent properly handles conversation history"""
    # Create a ChatAgent instance
    agent = ChatAgent()

    # Mock the stdio_client context manager
    with patch('agents.chat_agent.stdio_client') as mock_stdio_client:
        # Create a mock client
        mock_client = AsyncMock()
        mock_stdio_client.return_value.__aenter__.return_value = mock_client

        # Mock the call_tool response
        mock_result = MagicMock()
        mock_result.text = "Successfully created task 'Buy milk' with ID: 123e4567-e89b-12d3-a456-426614174003"
        mock_client.call_tool.return_value = [mock_result]

        # Process a message with conversation history
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        message = "Also add a task to buy milk"
        conversation_history = [
            {"role": "user", "content": "Add a task to buy groceries"},
            {"role": "assistant", "content": "I've added 'Buy groceries' to your task list."}
        ]

        result = await agent.process_message(user_id, message, conversation_history)

        # Verify that the result contains the expected response
        assert "response" in result
        assert "tool_calls" in result

        # Verify that the add_task tool was called
        assert result["tool_calls"][0]["name"] == "add_task"

        # Verify that the MCP client was called
        mock_client.call_tool.assert_called_once()


@pytest.mark.asyncio
async def test_agent_handles_error_in_mcp_call():
    """Test that the agent handles errors from MCP calls gracefully"""
    # Create a ChatAgent instance
    agent = ChatAgent()

    # Mock the stdio_client context manager
    with patch('agents.chat_agent.stdio_client') as mock_stdio_client:
        # Create a mock client
        mock_client = AsyncMock()
        mock_stdio_client.return_value.__aenter__.return_value = mock_client

        # Mock an exception from the MCP call
        mock_client.call_tool.side_effect = Exception("MCP server error")

        # Process a message that should trigger a tool call
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        message = "Add a task to buy groceries"

        result = await agent.process_message(user_id, message)

        # Verify that the result contains an error response
        assert "response" in result
        assert "error" in result["tool_results"][0]
        assert "MCP server error" in result["tool_results"][0]["error"]


@pytest.mark.asyncio
async def test_agent_handles_unknown_tool():
    """Test that the agent handles unknown tools gracefully"""
    # Create a ChatAgent instance
    agent = ChatAgent()

    # Mock the stdio_client context manager
    with patch('agents.chat_agent.stdio_client') as mock_stdio_client:
        # Create a mock client
        mock_client = AsyncMock()
        mock_stdio_client.return_value.__aenter__.return_value = mock_client

        # Mock the call_tool response to simulate an unknown tool scenario
        # In this case, we'll simulate the provider returning a call to an unknown tool
        # by patching the provider's process_message method
        with patch.object(agent.provider, 'process_message') as mock_provider_process:
            mock_provider_process.return_value = {
                "response": "I'll help you with that.",
                "tool_calls": [
                    {
                        "name": "unknown_tool",
                        "arguments": json.dumps({"user_id": "123e4567-e89b-12d3-a456-426614174000", "param": "value"})
                    }
                ]
            }

            # Process a message
            user_id = "123e4567-e89b-12d3-a456-426614174000"
            message = "Do something with unknown tool"

            result = await agent.process_message(user_id, message)

            # Verify that the result contains the expected response and error for unknown tool
            assert "response" in result
            assert len(result["tool_results"]) > 0
            assert "Unknown tool" in result["tool_results"][0]["result"]["error"]