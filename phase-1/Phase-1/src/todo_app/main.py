"""
Main entry point for the todo application.

This module provides the main function that serves as the entry point
for the command-line interface.

The main module integrates all components of the application and
provides the executable entry point for the todo application.
"""
from .cli import TodoCLI


def main():
    """Main entry point for the todo application."""
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()