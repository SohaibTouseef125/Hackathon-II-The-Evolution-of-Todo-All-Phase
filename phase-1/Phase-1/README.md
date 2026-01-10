# Phase 1 Todo In-Memory Python Console App

A simple command-line todo application with in-memory storage that supports all 5 Basic Level features (Add, Delete, Update, View, Mark Complete) using Python 3.13+.

## Features

- Add new tasks with titles and optional descriptions
- View all existing tasks with their status (pending/completed)
- Update existing task details
- Delete tasks by their unique identifier
- Mark tasks as complete or incomplete
- Interactive menu-driven interface with selection options
- Command-line interface for direct commands

## Prerequisites

- Python 3.13+
- UV package manager (optional, for dependency management)

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Install dependencies: `pip install -e .` or `uv sync`
4. Run the application: `uv run python -m src.todo_app.main`

## Usage

### Interactive Mode (Menu-driven UI)
Run without any arguments to enter the interactive menu:
```
uv run python -m src.todo_app.main
```
This will present a menu where you can select from:
1. Add Task
2. List Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit

### Command Line Mode
Direct commands:
- Add a task: `uv run python -m src.todo_app.main add "Task title" --description "Optional description"`
- List all tasks: `uv run python -m src.todo_app.main list`
- List pending tasks: `uv run python -m src.todo_app.main list --status pending`
- List completed tasks: `uv run python -m src.todo_app.main list --status completed`
- Update a task: `uv run python -m src.todo_app.main update 1 --title "New title" --description "New description"`
- Delete a task: `uv run python -m src.todo_app.main delete 1`
- Mark task complete: `uv run python -m src.todo_app.main complete 1`
- Mark task incomplete: `uv run python -m src.todo_app.main incomplete 1`

## Error Handling

The application provides helpful error messages for common issues:
- Invalid task IDs will result in "Task with ID X not found" messages
- Invalid titles (too short or too long) will result in validation error messages
- Missing required arguments will show usage information
- Other errors will be displayed with descriptive messages

## Development

To run tests: `uv run pytest`

## Architecture

- `src/todo_app/models.py` - Task and TaskList models
- `src/todo_app/services.py` - Business logic for task operations
- `src/todo_app/cli.py` - Command-line interface handlers with interactive menu
- `src/todo_app/main.py` - Entry point with CLI interface