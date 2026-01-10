"""Main entry point for Todo Extended CLI application.

Usage:
    # Interactive UI mode (colorful, menu-driven):
    python -m src.main
    todo

    # Command-line mode (traditional):
    python -m src.main <command> [options]
    todo <command> [options]

Commands (CLI mode):
    add         Add a new task
    list        List tasks with filters and sorting
    update      Update a task
    delete      Delete a task
    complete    Mark task as complete
    uncomplete  Mark task as not complete
    search      Search tasks by keyword
    reminders   Show tasks due soon or overdue
    config      View or set configuration

Examples:
    # Interactive mode
    todo

    # CLI mode
    todo add "Buy groceries" --priority high --tags shopping,urgent
    todo list --status pending --sort priority
    todo update 1 --priority low --tags home
    todo complete 1
    todo search "groceries"
    todo reminders
    todo config reminder-threshold 12h
"""

import sys
import argparse

from src.cli.parser import create_parser
from src.cli.commands import execute_command
from src.cli.ui import run_ui
from src.cli.ui import console


def main() -> int:
    """Main entry point for the CLI application.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Check if running in interactive mode (no arguments)
    if len(sys.argv) == 1:
        # Run interactive UI mode
        try:
            run_ui()
            return 0
        except KeyboardInterrupt:
            console.print("\n[info]Goodbye![/info]")
            return 0

    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    output = execute_command(args)
    print(output)

    # Return error code if output starts with "Error:"
    if output.startswith("Error:"):
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
