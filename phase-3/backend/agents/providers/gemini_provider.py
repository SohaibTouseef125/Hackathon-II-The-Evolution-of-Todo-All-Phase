from typing import Dict, Any, List
import os
import logging
import json
from ..provider_interface import AIProviderInterface


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeminiProvider(AIProviderInterface):
    """
    Google Gemini provider adapter implementing the AIProviderInterface.
    Uses Google's Gemini API with function calling capabilities to work with
    the OpenAI Agents SDK pattern.
    """

    def __init__(self):
        """
        Initialize the Gemini provider with API key from environment.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY environment variable is not set. Provider may not function properly.")
            # Use a placeholder key for initialization, but actual API calls will fail
            api_key = "AIza-placeholder-for-dev"

        # Import Google AI SDK
        try:
            import google.generativeai as genai
            self.genai = genai
            genai.configure(api_key=api_key)

            # Initialize the model
            # Use gemini-2.5-flash as it's the latest free model
            self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
            self.model = genai.GenerativeModel(self.model_name)
        except ImportError:
            raise ImportError(
                "Google Generative AI SDK is required for Gemini provider. "
                "Install it with: pip install google-generativeai"
            )

    def _convert_tools_to_gemini_format(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Convert OpenAI-style tools to Gemini-compatible function declarations.

        Args:
            tools: List of OpenAI-style tool definitions

        Returns:
            List of Gemini-compatible function declarations
        """
        gemini_tools = []

        for tool in tools:
            function_def = tool.get("function", {})
            name = function_def.get("name", "")
            description = function_def.get("description", "")
            parameters = function_def.get("parameters", {})

            # Convert OpenAI parameters to Gemini format
            gemini_function = {
                "name": name,
                "description": description,
                "parameters": parameters  # OpenAI and Gemini parameters format is compatible
            }

            gemini_tools.append({
                "function_declarations": [gemini_function]
            })

        return gemini_tools

    async def process_message(
        self,
        user_id: str,
        message: str,
        conversation_history: List[Dict[str, str]],
        tools: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Process a user message using Google's Gemini API with function calling.

        Args:
            user_id: The ID of the authenticated user
            message: The natural language message from the user
            conversation_history: List of previous messages for context
            tools: List of available tools that the AI can use

        Returns:
            Dictionary containing the response and any tool calls made
        """
        try:
            # Convert conversation history to Gemini-compatible format
            gemini_history = []
            for msg in conversation_history:
                role = msg.get("role", "user")
                # Map roles to Gemini format (user/model instead of user/assistant)
                gemini_role = "user" if role in ["user", "system"] else "model"

                gemini_history.append({
                    "role": gemini_role,
                    "parts": [msg.get("content", "")]  # Gemini expects parts as a list
                })

            # Add the current message to history
            gemini_history.append({
                "role": "user",
                "parts": [message]
            })

            # Convert tools to Gemini format
            gemini_tools = self._convert_tools_to_gemini_format(tools)

            # Create generation config
            generation_config = {
                "temperature": 0.7,
                "max_output_tokens": 2048,
            }

            # Generate content with tools
            response = self.model.generate_content(
                contents=gemini_history,
                tools=gemini_tools,
                tool_config={'function_calling_config': {'mode': 'ANY'}},  # Enable function calling
                generation_config=generation_config
            )

            # Process the response
            tool_calls = []
            tool_results = []

            # Check if the response contains function calls
            if hasattr(response.candidates[0], 'content') and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'function_call'):
                        # Extract function call information
                        function_call = part.function_call
                        args_dict = {}

                        # Convert the protobuf args to dictionary
                        for key, value in function_call.args.items():
                            args_dict[key] = value

                        tool_call_data = {
                            "name": function_call.name,
                            "arguments": json.dumps(args_dict)
                        }

                        tool_calls.append(tool_call_data)

                        # Add to tool results
                        tool_results.append({
                            "name": function_call.name,
                            "arguments": json.dumps(args_dict)
                        })

            # Get the text response
            text_response = ""
            try:
                # Try to get the text response if available
                if hasattr(response, 'text'):
                    text_response = response.text
            except:
                # If .text fails (e.g., when there are function calls), parse parts manually
                pass

            if not text_response and hasattr(response.candidates[0], 'content') and response.candidates[0].content.parts:
                # Concatenate all text parts
                text_parts = []
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'text') and part.text:
                        text_parts.append(part.text)
                text_response = " ".join(text_parts)

            if not text_response and tool_calls:
                text_response = "Processing your request with the required tools..."

            return {
                "response": text_response or "I processed your request.",
                "tool_calls": tool_calls,
                "tool_results": tool_results
            }

        except Exception as e:
            logger.error(f"Error processing message with Gemini for user {user_id}: {str(e)}")
            return {
                "response": "Sorry, I encountered an error processing your request.",
                "tool_calls": [],
                "tool_results": [{"error": str(e)}]
            }

    async def validate_configuration(self) -> bool:
        """
        Validate that the Gemini provider is properly configured.

        Returns:
            Boolean indicating if the configuration is valid
        """
        try:
            # Attempt a simple API call to validate the configuration
            response = self.model.generate_content("Hello")
            return response.text is not None
        except Exception as e:
            logger.error(f"Gemini configuration validation failed: {str(e)}")
            return False

    def get_provider_info(self) -> Dict[str, str]:
        """
        Get information about the Gemini provider.

        Returns:
            Dictionary containing provider information
        """
        return {
            "name": "Google Gemini",
            "model": self.model_name,
            "type": "cloud"
        }