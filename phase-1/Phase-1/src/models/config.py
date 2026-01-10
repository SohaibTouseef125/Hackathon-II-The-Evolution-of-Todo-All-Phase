"""Configuration model for Todo Extended application.

This module defines the global configuration settings.
"""

from dataclasses import dataclass, field
from datetime import timedelta
import re


@dataclass
class Config:
    """Global configuration for the application.

    Attributes:
        reminder_threshold: Time before due date to show reminder (default: 24h)
    """

    reminder_threshold: timedelta = field(default_factory=lambda: timedelta(hours=24))

    # Valid threshold formats
    _VALID_THRESHOLDS = {"1h", "6h", "12h", "24h", "48h", "7d"}

    def set_threshold(self, value: str) -> None:
        """Parse and set threshold from string like '24h', '7d'.

        Args:
            value: Threshold string in format '<number>h' or '<number>d'

        Raises:
            ValueError: If format is invalid or value not in allowed set
        """
        if not value:
            raise ValueError("Threshold cannot be empty")

        # Validate format
        if not re.match(r"^\d+[hd]$", value):
            raise ValueError(
                f"Invalid threshold format: {value}. Use: 1h, 6h, 12h, 24h, 48h, 7d"
            )

        if value.endswith("h"):
            hours = int(value[:-1])
            self.reminder_threshold = timedelta(hours=hours)
        elif value.endswith("d"):
            days = int(value[:-1])
            self.reminder_threshold = timedelta(days=days)
        else:
            raise ValueError(
                f"Invalid threshold format: {value}. Use: 1h, 6h, 12h, 24h, 48h, 7d"
            )

    def get_threshold_display(self) -> str:
        """Return human-readable threshold string.

        Returns:
            String representation like '24h' or '7d'
        """
        total_hours = self.reminder_threshold.total_seconds() / 3600

        # Only show days for 7d (168h), otherwise show hours
        if total_hours == 168:  # 7 days
            return "7d"
        else:
            return f"{int(total_hours)}h"


# Global config instance
_config: Config | None = None


def get_config() -> Config:
    """Get or create the global config instance.

    Returns:
        Global Config instance
    """
    global _config
    if _config is None:
        _config = Config()
    return _config


def reset_config() -> None:
    """Reset config to defaults (useful for testing)."""
    global _config
    _config = None
