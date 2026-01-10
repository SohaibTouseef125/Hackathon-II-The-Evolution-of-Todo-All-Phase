"""Command handlers for CLI.

This module provides the execute_command function and individual command handlers.
"""

import argparse
from typing import Optional

from src.models.task import Priority, Recurrence
from src.models.config import get_config
from src.services.task_store import get_store
from src.services.task_service import TaskService
from src.cli.formatters import (
    format_task_created,
    format_task_updated,
    format_task_deleted,
    format_task_completed,
    format_task_list,
    format_search_results,
    format_filter_results,
    format_reminder_list,
    format_config,
    format_error,
)


def execute_command(args: argparse.Namespace) -> str:
    """Execute a CLI command based on parsed arguments.

    Args:
        args: Parsed command-line arguments

    Returns:
        Command output string
    """
    store = get_store()
    service = TaskService(store)

    if args.command == "add":
        return cmd_add(args, service)
    elif args.command == "list":
        return cmd_list(args, service)
    elif args.command == "update":
        return cmd_update(args, service)
    elif args.command == "delete":
        return cmd_delete(args, service)
    elif args.command == "complete":
        return cmd_complete(args, service)
    elif args.command == "uncomplete":
        return cmd_uncomplete(args, service)
    elif args.command == "search":
        return cmd_search(args, service)
    elif args.command == "reminders":
        return cmd_reminders(args, service)
    elif args.command == "config":
        return cmd_config(args, service)
    else:
        return "Unknown command. Use --help for usage information."


def cmd_add(args: argparse.Namespace, service: TaskService) -> str:
    """Handle add command.

    Args:
        args: Parsed arguments
        service: TaskService instance

    Returns:
        Command output
    """
    try:
        # Validate and parse inputs
        priority = service.validate_priority(args.priority)
        tags = service.validate_tags(args.tags) if args.tags else []
        due_date = service.validate_due_date(args.due) if args.due else None
        due_time = service.validate_due_time(args.time, due_date is not None)
        recurrence = service.validate_recurrence(args.recurrence, due_date is not None)

        # Create task
        task = service.create_task(
            title=args.title,
            description=args.description,
            priority=priority,
            tags=tags,
            due_date=due_date,
            due_time=due_time,
            recurrence=recurrence,
        )

        return format_task_created(task)

    except ValueError as e:
        return format_error(str(e))


def cmd_list(args: argparse.Namespace, service: TaskService) -> str:
    """Handle list command.

    Args:
        args: Parsed arguments
        service: TaskService instance

    Returns:
        Command output
    """
    # Filter tasks
    tasks = service.filter_tasks(
        status=args.status,
        priority=args.priority,
        due=args.due,
    )

    # Sort tasks
    tasks = service.sort_tasks(tasks, sort_by=args.sort, reverse=args.reverse)

    return format_filter_results(
        tasks,
        service,
        status=args.status,
        priority=args.priority,
        due=args.due,
    )


def cmd_update(args: argparse.Namespace, service: TaskService) -> str:
    """Handle update command.

    Args:
        args: Parsed arguments
        service: TaskService instance

    Returns:
        Command output
    """
    try:
        # Get current task to check for due_date
        task = service.get_task(args.id)

        # Validate inputs if provided
        priority = None
        if args.priority:
            priority = service.validate_priority(args.priority)

        tags = None
        if args.tags is not None:
            tags = service.validate_tags(args.tags)

        due_date = None
        if args.due is not None:
            if args.due.lower() == "none":
                due_date = "none"  # Sentinel to clear
            else:
                due_date = service.validate_due_date(args.due)

        # Determine if we have a due date for time validation
        has_due_date = (
            due_date not in (None, "none")
            or (due_date is None and task.due_date is not None)
        )

        due_time = None
        if args.time is not None:
            if args.time.lower() == "none":
                due_time = "none"  # Sentinel to clear
            else:
                due_time = service.validate_due_time(args.time, has_due_date)

        # Validate recurrence
        recurrence = None
        if args.recurrence:
            # Determine if task will have due date after update
            final_has_due = has_due_date if due_date != "none" else False
            recurrence = service.validate_recurrence(args.recurrence, final_has_due)

        # Update task
        updated = service.update_task(
            task_id=args.id,
            title=args.title,
            description=args.description,
            priority=priority,
            tags=tags,
            due_date=due_date,
            due_time=due_time,
            recurrence=recurrence,
        )

        return format_task_updated(updated)

    except ValueError as e:
        return format_error(str(e))


def cmd_delete(args: argparse.Namespace, service: TaskService) -> str:
    """Handle delete command.

    Args:
        args: Parsed arguments
        service: TaskService instance

    Returns:
        Command output
    """
    try:
        service.delete_task(args.id)
        return format_task_deleted(args.id)

    except ValueError as e:
        return format_error(str(e))


def cmd_complete(args: argparse.Namespace, service: TaskService) -> str:
    """Handle complete command.

    Args:
        args: Parsed arguments
        service: TaskService instance

    Returns:
        Command output
    """
    try:
        task, new_task = service.complete_task(args.id)
        return format_task_completed(task, new_task)

    except ValueError as e:
        return format_error(str(e))


def cmd_uncomplete(args: argparse.Namespace, service: TaskService) -> str:
    """Handle uncomplete command.

    Args:
        args: Parsed arguments
        service: TaskService instance

    Returns:
        Command output
    """
    try:
        task = service.uncomplete_task(args.id)
        return format_task_updated(task)

    except ValueError as e:
        return format_error(str(e))


def cmd_search(args: argparse.Namespace, service: TaskService) -> str:
    """Handle search command.

    Args:
        args: Parsed arguments
        service: TaskService instance

    Returns:
        Command output
    """
    tasks = service.search_tasks(args.keyword)
    return format_search_results(tasks, args.keyword)


def cmd_reminders(args: argparse.Namespace, service: TaskService) -> str:
    """Handle reminders command.

    Args:
        args: Parsed arguments
        service: TaskService instance

    Returns:
        Command output
    """
    tasks = service.get_reminder_tasks()
    return format_reminder_list(tasks, service)


def cmd_config(args: argparse.Namespace, service: TaskService) -> str:
    """Handle config command.

    Args:
        args: Parsed arguments
        service: TaskService instance

    Returns:
        Command output
    """
    config = get_config()

    if args.setting is None:
        # Show current configuration
        settings = {
            "reminder_threshold": config.get_threshold_display(),
        }
        return format_config(settings)

    if args.setting == "reminder-threshold":
        if args.value is None:
            return format_error("Value required for reminder-threshold")

        try:
            config.set_threshold(args.value)
            return f"Reminder threshold set to {args.value}"
        except ValueError as e:
            return format_error(str(e))

    return format_error(f"Unknown setting: {args.setting}")
