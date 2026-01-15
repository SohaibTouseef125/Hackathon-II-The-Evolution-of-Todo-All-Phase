"""
Agent Runner for Todo AI Chatbot

This module implements the agent runner that manages the execution of the
AI agent and coordinates with the MCP server for tool execution.
"""

from typing import Dict, Any, List
from .chat_agent import chat_agent
import logging
import json
from mcp.client.stdio import stdio_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentRunner:
    """
    Runs the AI agent and manages the interaction between the chat interface
    and the MCP tools for task operations.
    """

    def __init__(self):
        """
        Initialize the agent runner with the chat agent.
        """
        self.agent = chat_agent
        logger.info("AgentRunner initialized")

    async def run_conversation(self, user_id: str, message: str, conversation_history: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run a conversation turn with the AI agent.

        Args:
            user_id: The ID of the authenticated user
            message: The user's message
            conversation_history: Previous conversation history

        Returns:
            Dictionary containing the agent's response and any tool calls made
        """
        try:
            logger.info(f"Running conversation for user {user_id} with message: {message[:50]}...")

            # Process the message using the chat agent
            result = await self.agent.process_message(
                user_id=user_id,
                message=message,
                conversation_history=conversation_history
            )

            logger.info(f"Agent response generated for user {user_id}")

            return result

        except Exception as e:
            logger.error(f"Error running conversation for user {user_id}: {str(e)}")
            return {
                "response": "I'm having trouble processing your request right now. The system may need to be configured properly or there could be an issue with the AI provider or tools.",
                "tool_calls": [],
                "tool_results": [{"error": str(e)}]
            }

    async def execute_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a specific tool call with the given arguments.

        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool

        Returns:
            Result of the tool execution
        """
        try:
            logger.info(f"Executing tool call: {tool_name} with args: {arguments}")

            # Connect to the MCP server and execute the tool
            async with stdio_client() as client:
                result = await client.call_tool(tool_name, arguments)

                # Parse the result from the MCP server
                if result and len(result) > 0:
                    text_content = result[0].text
                    return {
                        "status": "success",
                        "message": text_content,
                        "original_arguments": arguments
                    }
                else:
                    return {"status": "error", "message": "No response from MCP server"}

        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            # Return a structured error response that won't break the flow
            return {
                "status": "error",
                "message": f"Tool execution failed: {str(e)}. This may indicate the MCP server is not running.",
                "original_arguments": arguments
            }

    async def validate_user_access(self, user_id: str, target_user_id: str) -> bool:
        """
        Validate that the authenticated user has access to perform operations
        on the specified user's data.

        Args:
            user_id: The authenticated user's ID
            target_user_id: The ID of the user whose data is being accessed

        Returns:
            Boolean indicating if access is allowed
        """
        try:
            # In a real implementation, we might perform additional validation
            # For now, we just compare the IDs directly
            is_valid = user_id == target_user_id
            if not is_valid:
                logger.warning(f"Access denied: user {user_id} attempted to access data for user {target_user_id}")
            return is_valid
        except Exception as e:
            logger.error(f"Error validating user access: {str(e)}")
            return False

# Singleton instance
agent_runner = AgentRunner()

async def get_runner():
    """Get the agent runner instance."""
    return agent_runner