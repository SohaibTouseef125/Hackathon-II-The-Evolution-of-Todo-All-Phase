---
name: todo-console-app
description: Comprehensive Python console todo application with in-memory storage. Use when Claude needs to work with the Phase I Hackathon II todo console app for creating basic todo functionality (add, delete, update, view, mark complete), implementing Python console applications with clean architecture, building in-memory data structures for todo management, following spec-driven development practices, or any other Phase I todo console app tasks.
---

# Todo Console App - Phase I

## Overview

This skill provides comprehensive guidance for building a Python console-based todo application as part of Hackathon II Phase I. It covers the basic 5 todo operations (Add, Delete, Update, View, Mark Complete) with in-memory storage using Python 3.13+ and following clean code principles.

## Core Capabilities

### 1. Todo Operations Implementation
- Add new todo tasks with title and description
- Delete existing todo tasks by ID
- Update todo task details (title, description)
- View all todo tasks with status indicators
- Mark tasks as complete/incomplete

### 2. Data Management
- In-memory storage using Python data structures
- Task ID generation and management
- Task status tracking (pending/complete)
- Data persistence simulation

### 3. Console Interface
- Command-line user interface
- Menu-driven navigation
- Input validation and error handling
- User-friendly prompts and feedback

### 4. Spec-Driven Development
- Integration with Claude Code and Spec-Kit Plus
- Following spec-driven implementation patterns
- Clean project structure and organization
- Proper Python project conventions

## Project Structure

### Recommended Directory Structure
```
todo-console-app/
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point and main loop
│   ├── todo_manager.py      # Core todo operations
│   ├── models.py            # Task data model
│   └── cli.py               # Command-line interface
├── tests/
│   ├── __init__.py
│   ├── test_todo_manager.py
│   └── test_cli.py
├── specs/
│   ├── todo-spec.md
│   └── architecture.md
├── CLAUDE.md
├── pyproject.toml
└── README.md
```

## Implementation Guidelines

### 1. Task Model (models.py)
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
```

### 2. Todo Manager (todo_manager.py)
```python
from typing import List, Optional
from .models import Task

class TodoManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self._next_id = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        task = Task(
            id=self._next_id,
            title=title,
            description=description
        )
        self.tasks.append(task)
        self._next_id += 1
        return task

    def delete_task(self, task_id: int) -> bool:
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                return True
        return False

    def update_task(self, task_id: int, title: Optional[str] = None,
                   description: Optional[str] = None) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                if title is not None:
                    task.title = title
                if description is not None:
                    task.description = description
                return task
        return None

    def get_task(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_all_tasks(self) -> List[Task]:
        return self.tasks.copy()

    def mark_complete(self, task_id: int, completed: bool = True) -> bool:
        task = self.get_task(task_id)
        if task:
            task.completed = completed
            return True
        return False
```

### 3. CLI Interface (cli.py)
```python
from typing import Optional
from .todo_manager import TodoManager

class TodoCLI:
    def __init__(self, todo_manager: TodoManager):
        self.manager = todo_manager

    def display_menu(self):
        print("\n=== Todo Console App ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete")
        print("6. Mark Task Incomplete")
        print("7. Exit")
        print("========================")

    def get_user_choice(self) -> str:
        return input("Enter your choice (1-7): ").strip()

    def add_task(self):
        title = input("Enter task title: ").strip()
        if not title:
            print("Title cannot be empty!")
            return

        description = input("Enter task description (optional): ").strip()
        description = description if description else None

        task = self.manager.add_task(title, description)
        print(f"Task added successfully! ID: {task.id}")

    def view_tasks(self):
        tasks = self.manager.get_all_tasks()
        if not tasks:
            print("No tasks found!")
            return

        print("\nYour Tasks:")
        print("-" * 50)
        for task in tasks:
            status = "✓" if task.completed else "○"
            print(f"[{status}] ID: {task.id} | {task.title}")
            if task.description:
                print(f"      Description: {task.description}")
            print(f"      Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}")
            print()

    def update_task(self):
        try:
            task_id = int(input("Enter task ID to update: "))
        except ValueError:
            print("Invalid task ID!")
            return

        task = self.manager.get_task(task_id)
        if not task:
            print("Task not found!")
            return

        new_title = input(f"Enter new title (current: {task.title}): ").strip()
        new_title = new_title if new_title else None

        new_desc = input(f"Enter new description (current: {task.description or 'None'}): ").strip()
        new_desc = new_desc if new_desc else None

        updated_task = self.manager.update_task(task_id, new_title, new_desc)
        if updated_task:
            print("Task updated successfully!")
        else:
            print("Failed to update task!")

    def delete_task(self):
        try:
            task_id = int(input("Enter task ID to delete: "))
        except ValueError:
            print("Invalid task ID!")
            return

        if self.manager.delete_task(task_id):
            print("Task deleted successfully!")
        else:
            print("Task not found!")

    def mark_task_complete(self, completed: bool = True):
        try:
            task_id = int(input("Enter task ID to mark: "))
        except ValueError:
            print("Invalid task ID!")
            return

        if self.manager.mark_complete(task_id, completed):
            status = "complete" if completed else "incomplete"
            print(f"Task marked as {status}!")
        else:
            print("Task not found!")

    def run(self):
        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.view_tasks()
            elif choice == "3":
                self.update_task()
            elif choice == "4":
                self.delete_task()
            elif choice == "5":
                self.mark_task_complete(True)
            elif choice == "6":
                self.mark_task_complete(False)
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid choice! Please try again.")
```

### 4. Main Application (main.py)
```python
#!/usr/bin/env python3
"""
Todo Console Application - Phase I
A simple console-based todo application with in-memory storage.
"""
from src.todo_manager import TodoManager
from src.cli import TodoCLI

def main():
    # Initialize the todo manager and CLI
    todo_manager = TodoManager()
    cli = TodoCLI(todo_manager)

    # Run the application
    cli.run()

if __name__ == "__main__":
    main()
```

## Spec-Driven Development Workflow

### 1. Specification Creation
- Create feature specifications in `/specs/`
- Define acceptance criteria before implementation
- Use Spec-Kit Plus for structured specs

### 2. Implementation Process
1. Read the relevant specification
2. Generate implementation plan
3. Break down into specific tasks
4. Use Claude Code to implement based on spec

### 3. Testing Strategy
- Unit tests for core functionality
- Integration tests for CLI interactions
- Edge case testing (empty inputs, invalid IDs)

## Basic Todo Operations

### 1. Add Task
- Validate title is not empty
- Generate unique ID
- Set creation timestamp
- Return created task

### 2. Delete Task
- Find task by ID
- Remove from collection
- Return success status

### 3. Update Task
- Find task by ID
- Update specified fields only
- Preserve unchanged fields
- Return updated task

### 4. View Tasks
- List all tasks with status indicators
- Show completion status (✓/○)
- Include timestamps and descriptions

### 5. Mark Complete/Incomplete
- Toggle completion status
- Update task state
- Return success status

## Python Best Practices

### 1. Code Quality
- Use type hints for all functions
- Follow PEP 8 style guidelines
- Write clear, descriptive variable names
- Include docstrings for classes and functions

### 2. Error Handling
- Validate user inputs
- Handle edge cases gracefully
- Provide informative error messages
- Prevent application crashes

### 3. Project Structure
- Separate concerns into modules
- Use proper imports
- Follow Python packaging conventions
- Include proper `__init__.py` files

## Command Line Usage

### Running the Application
```bash
python src/main.py
```

### Alternative Entry Point
```bash
cd todo-console-app
python -m src.main
```

## Resources

### references/
- `todo_specification.md` - Detailed feature specifications
- `python_best_practices.md` - Python coding standards and patterns
- `spec_driven_development.md` - Spec-Kit Plus workflow and practices
- `testing_strategies.md` - Unit and integration testing approaches

### assets/
- `project_templates/` - Project structure templates
- `spec_templates/` - Specification document templates
- `test_templates/` - Testing framework templates
