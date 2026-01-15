from enum import Enum
from typing import Literal
import os
from dotenv import load_dotenv
load_dotenv()


class AIProviderType(str, Enum):
    OPENAI = "openai"
    GEMINI = "gemini"
    OPENROUTER = "openrouter"


# Configuration for AI provider selection
AI_PROVIDER: AIProviderType = AIProviderType(os.getenv("AI_PROVIDER", "openrouter"))

# Model configuration
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")


def get_selected_provider() -> AIProviderType:
    """
    Get the currently selected AI provider based on environment configuration.

    Returns:
        AIProviderType: The selected provider type
    """
    return AI_PROVIDER


def is_openai_selected() -> bool:
    """
    Check if OpenAI is the selected provider.

    Returns:
        bool: True if OpenAI is selected, False otherwise
    """
    return AI_PROVIDER == AIProviderType.OPENAI


def is_gemini_selected() -> bool:
    """
    Check if Gemini is the selected provider.

    Returns:
        bool: True if Gemini is selected, False otherwise
    """
    return AI_PROVIDER == AIProviderType.GEMINI


def is_openrouter_selected() -> bool:
    """
    Check if OpenRouter is the selected provider.

    Returns:
        bool: True if OpenRouter is selected, False otherwise
    """
    return AI_PROVIDER == AIProviderType.OPENROUTER