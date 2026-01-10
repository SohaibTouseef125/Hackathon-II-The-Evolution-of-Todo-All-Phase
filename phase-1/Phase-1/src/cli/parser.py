"""CLI argument parser setup.

This module provides the argument parser for the todo command.
"""

import argparse


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the todo CLI.

    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog="todo",
        description="Todo Extended - Phase 1 Console Application",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ==================== Add Command ====================
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument(
        "-d", "--description",
        help="Task description",
        default=None,
    )
    add_parser.add_argument(
        "-p", "--priority",
        help="Task priority (high, medium, low)",
        choices=["high", "medium", "low"],
        default="medium",
    )
    add_parser.add_argument(
        "-t", "--tags",
        help="Comma-separated tags",
        default=None,
    )
    add_parser.add_argument(
        "--due",
        help="Due date (YYYY-MM-DD)",
        default=None,
    )
    add_parser.add_argument(
        "--time",
        help="Due time (HH:MM)",
        default=None,
    )
    add_parser.add_argument(
        "-r", "--recurrence",
        help="Recurrence pattern (daily, weekly, monthly, none)",
        choices=["daily", "weekly", "monthly", "none"],
        default="none",
    )

    # ==================== List Command ====================
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument(
        "-s", "--status",
        help="Filter by status",
        choices=["all", "pending", "completed"],
        default="all",
    )
    list_parser.add_argument(
        "-p", "--priority",
        help="Filter by priority",
        choices=["all", "high", "medium", "low"],
        default="all",
    )
    list_parser.add_argument(
        "--due",
        help="Filter by due date",
        choices=["all", "today", "week", "overdue"],
        default="all",
    )
    list_parser.add_argument(
        "--sort",
        help="Sort by field",
        choices=["created", "due_date", "priority", "title"],
        default="created",
    )
    list_parser.add_argument(
        "--reverse",
        help="Reverse sort order",
        action="store_true",
    )

    # ==================== Update Command ====================
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument(
        "-T", "--title",
        help="New title",
        default=None,
    )
    update_parser.add_argument(
        "-d", "--description",
        help="New description",
        default=None,
    )
    update_parser.add_argument(
        "-p", "--priority",
        help="New priority",
        choices=["high", "medium", "low"],
        default=None,
    )
    update_parser.add_argument(
        "-t", "--tags",
        help="New tags (comma-separated)",
        default=None,
    )
    update_parser.add_argument(
        "--due",
        help="New due date (YYYY-MM-DD or 'none' to remove)",
        default=None,
    )
    update_parser.add_argument(
        "--time",
        help="New due time (HH:MM or 'none' to remove)",
        default=None,
    )
    update_parser.add_argument(
        "-r", "--recurrence",
        help="New recurrence pattern",
        choices=["daily", "weekly", "monthly", "none"],
        default=None,
    )

    # ==================== Delete Command ====================
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    # ==================== Complete Command ====================
    complete_parser = subparsers.add_parser("complete", help="Mark task as complete")
    complete_parser.add_argument("id", type=int, help="Task ID")

    # ==================== Uncomplete Command ====================
    uncomplete_parser = subparsers.add_parser(
        "uncomplete", help="Mark task as not complete"
    )
    uncomplete_parser.add_argument("id", type=int, help="Task ID")

    # ==================== Search Command ====================
    search_parser = subparsers.add_parser("search", help="Search tasks")
    search_parser.add_argument("keyword", help="Search keyword")

    # ==================== Reminders Command ====================
    subparsers.add_parser("reminders", help="Show tasks due soon or overdue")

    # ==================== Config Command ====================
    config_parser = subparsers.add_parser("config", help="View or set configuration")
    config_parser.add_argument(
        "setting",
        nargs="?",
        help="Setting to change (e.g., 'reminder-threshold')",
        default=None,
    )
    config_parser.add_argument(
        "value",
        nargs="?",
        help="New value for setting",
        default=None,
    )

    return parser
