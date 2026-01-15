import logging
from datetime import datetime
import sys
import os
from typing import Optional


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up comprehensive logging for the application.

    Args:
        level: Logging level (default: logging.INFO)
        log_file: Optional file path to write logs to
        format_string: Optional custom format string

    Returns:
        Configured logger instance
    """
    if format_string is None:
        format_string = (
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
        )

    # Create formatter
    formatter = logging.Formatter(format_string)

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # Clear any existing handlers
    logger.handlers.clear()

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create file handler if specified
    if log_file:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a named logger instance.

    Args:
        name: Name of the logger

    Returns:
        Named logger instance
    """
    return logging.getLogger(name)


def log_performance(
    logger: logging.Logger,
    operation: str,
    duration: float,
    user_id: Optional[str] = None,
    success: bool = True
) -> None:
    """
    Log performance metrics for operations.

    Args:
        logger: Logger instance to use
        operation: Name of the operation being measured
        duration: Duration of the operation in seconds
        user_id: Optional user ID for the operation
        success: Whether the operation was successful
    """
    status = "SUCCESS" if success else "FAILED"
    user_info = f" user={user_id}" if user_id else ""
    logger.info(
        f"PERFORMANCE operation={operation} status={status} "
        f"duration={duration:.3f}s{user_info}"
    )


def log_error_with_context(
    logger: logging.Logger,
    error: Exception,
    context: dict,
    level: int = logging.ERROR
) -> None:
    """
    Log an error with additional context information.

    Args:
        logger: Logger instance to use
        error: Exception that occurred
        context: Dictionary with context information
        level: Logging level for the error
    """
    context_str = " ".join([f"{k}={v}" for k, v in context.items()])
    logger.log(
        level,
        f"ERROR type={type(error).__name__} message={str(error)} {context_str}"
    )


# Initialize application logger
app_logger = setup_logging(
    level=logging.INFO,
    log_file="logs/app.log"
)


def get_app_logger() -> logging.Logger:
    """
    Get the application-wide logger instance.

    Returns:
        Application logger instance
    """
    return app_logger