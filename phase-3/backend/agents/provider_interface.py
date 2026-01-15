from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import uuid


class AIProviderInterface(ABC):
    """
    Abstract interface for AI providers to ensure consistent implementation
    across different AI services (OpenAI, Google Gemini, etc.)
    """

    @abstractmethod
    async def process_message(
        self,
        user_id: str,
        message: str,
        conversation_history: List[Dict[str, str]],
        tools: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Process a user message and return AI response with tool calls if needed.

        Args:
            user_id: The ID of the authenticated user
            message: The natural language message from the user
            conversation_history: List of previous messages for context
            tools: List of available tools that the AI can use

        Returns:
            Dictionary containing the response and any tool calls made
        """
        pass

    @abstractmethod
    async def validate_configuration(self) -> bool:
        """
        Validate that the provider is properly configured with required credentials.

        Returns:
            Boolean indicating if the configuration is valid
        """
        pass

    @abstractmethod
    def get_provider_info(self) -> Dict[str, str]:
        """
        Get information about the AI provider.

        Returns:
            Dictionary containing provider information
        """
        pass