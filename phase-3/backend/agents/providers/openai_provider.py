from typing import Dict, Any, List, Optional
from openai import OpenAI
import os
import logging
from ..provider_interface import AIProviderInterface


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenAIProvider(AIProviderInterface):
    """
    OpenAI provider adapter implementing the AIProviderInterface.
    Uses OpenAI's API with function calling capabilities for tool integration.
    """

    def __init__(self):
        """
        Initialize the OpenAI provider with API key from environment.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

    async def process_message(
        self,
        user_id: str,
        message: str,
        conversation_history: List[Dict[str, str]],
        tools: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Process a user message using OpenAI's API with function calling.

        Args:
            user_id: The ID of the authenticated user
            message: The natural language message from the user
            conversation_history: List of previous messages for context
            tools: List of available tools that the AI can use

        Returns:
            Dictionary containing the response and any tool calls made
        """
        try:
            # Prepare messages for the AI model
            messages = []

            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)

            # Add the current user message
            messages.append({"role": "user", "content": message})

            # Call the OpenAI API with the defined tools
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto",  # Let the model decide when to use tools
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # Process tool calls if any were made
            tool_results = []
            if tool_calls:
                for tool_call in tool_calls:
                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    })

            return {
                "response": response_message.content or "I processed your request.",
                "tool_calls": [
                    {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    } for tc in tool_calls
                ] if tool_calls else [],
                "tool_results": tool_results
            }

        except Exception as e:
            logger.error(f"Error processing message with OpenAI for user {user_id}: {str(e)}")
            return {
                "response": "Sorry, I encountered an error processing your request.",
                "tool_calls": [],
                "tool_results": [{"error": str(e)}]
            }

    async def validate_configuration(self) -> bool:
        """
        Validate that the OpenAI provider is properly configured.

        Returns:
            Boolean indicating if the configuration is valid
        """
        try:
            # Attempt a simple API call to validate the configuration
            self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            logger.error(f"OpenAI configuration validation failed: {str(e)}")
            return False

    def get_provider_info(self) -> Dict[str, str]:
        """
        Get information about the OpenAI provider.

        Returns:
            Dictionary containing provider information
        """
        return {
            "name": "OpenAI",
            "model": self.model,
            "type": "cloud"
        }