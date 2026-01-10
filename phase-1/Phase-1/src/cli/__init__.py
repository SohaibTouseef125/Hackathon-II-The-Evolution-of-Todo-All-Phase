"""CLI interface for Todo Extended application."""

from src.cli.parser import create_parser
from src.cli.commands import execute_command
from src.cli.formatters import (
    format_task,
    format_task_list,
    format_task_created,
    format_task_updated,
    format_task_deleted,
    format_task_completed,
    format_search_results,
    format_filter_results,
    format_reminder_list,
    format_config,
    format_error,
)

__all__ = [
    "create_parser",
    "execute_command",
    "format_task",
    "format_task_list",
    "format_task_created",
    "format_task_updated",
    "format_task_deleted",
    "format_task_completed",
    "format_search_results",
    "format_filter_results",
    "format_reminder_list",
    "format_config",
    "format_error",
]
