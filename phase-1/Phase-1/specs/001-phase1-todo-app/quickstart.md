# Quickstart Guide: Phase 1 Todo In-Memory Python Console App

## Prerequisites
- Python 3.13+
- UV package manager (optional)

## Setup
1. Clone the repository
2. Navigate to the project directory
3. Install dependencies: `pip install -e .` or `uv sync`
4. Run the application: `uv run python -m src.todo_app.main`

## Basic Usage
- Add a task: `uv run python -m src.todo_app.main add "Task title" --description "Optional description"`
- List all tasks: `uv run python -m src.todo_app.main list`
- List pending tasks: `uv run python -m src.todo_app.main list --status pending`
- List completed tasks: `uv run python -m src.todo_app.main list --status completed`
- Update a task: `uv run python -m src.todo_app.main update 1 --title "New title" --description "New description"`
- Delete a task: `uv run python -m src.todo_app.main delete 1`
- Mark task complete: `uv run python -m src.todo_app.main complete 1`
- Mark task incomplete: `uv run python -m src.todo_app.main incomplete 1`

## Example Workflow
1. Add a task: `uv run python -m src.todo_app.main add "Buy groceries" --description "Milk, eggs, bread"`
2. List tasks: `uv run python -m src.todo_app.main list`
3. Mark task complete: `uv run python -m src.todo_app.main complete 1`
4. List tasks again to see the updated status

## Testing
Run all tests: `uv run pytest`
Run specific test file: `uv run pytest tests/test_models.py`

## Architecture
- `src/todo_app/models.py` - Task and TaskList models with validation
- `src/todo_app/services.py` - Business logic for task operations
- `src/todo_app/cli.py` - Command-line interface handlers
- `src/todo_app/main.py` - Entry point for the application