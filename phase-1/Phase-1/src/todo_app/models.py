"""
Task and TaskList models for the todo application.

This module contains the core data models for the todo app:
- Task: Represents a single todo item
- TaskList: Collection of Task objects with operations

The models implement all validation rules and business logic for task management
in an in-memory storage system.
"""
from datetime import datetime
from typing import List, Optional


class Task:
    """
    Represents a single todo item with unique ID, title, description, and completion status.
    """
    def __init__(self, id: int, title: str, description: str = "", completed: bool = False):
        """
        Initialize a Task object.

        Args:
            id: Unique identifier for the task
            title: Title of the task (required, 1-200 characters)
            description: Optional description of the task (max 1000 characters)
            completed: Completion status of the task (default: False)
        """
        self.id = id
        self.title = self._validate_title(title)
        self.description = self._validate_description(description)
        self.completed = completed
        self.created_at = datetime.now()

    def _validate_title(self, title: str) -> str:
        """Validate the title length (1-200 characters)."""
        if not isinstance(title, str):
            raise ValueError("Title must be a string")
        if len(title) < 1 or len(title) > 200:
            raise ValueError("Title must be between 1 and 200 characters")
        return title

    def _validate_description(self, description: str) -> str:
        """Validate the description length (0-1000 characters)."""
        if not isinstance(description, str):
            raise ValueError("Description must be a string")
        if len(description) > 1000:
            raise ValueError("Description must be 1000 characters or less")
        return description

    def update(self, title: Optional[str] = None, description: Optional[str] = None) -> None:
        """
        Update task properties.

        Args:
            title: New title (optional)
            description: New description (optional)
        """
        if title is not None:
            self.title = self._validate_title(title)
        if description is not None:
            self.description = self._validate_description(description)

    def to_dict(self) -> dict:
        """Convert task to dictionary representation."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }


class TaskList:
    """
    Collection of tasks stored in memory during the application session.
    """
    def __init__(self):
        """Initialize an empty TaskList."""
        self.tasks: List[Task] = []
        self.next_id = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Create new task with unique ID and add to collection.

        Args:
            title: Title of the task
            description: Optional description of the task

        Returns:
            The newly created Task object
        """
        if len(self.tasks) >= 100:
            raise ValueError("Maximum number of tasks (100) reached")

        task = Task(self.next_id, title, description)
        self.tasks.append(task)
        self.next_id += 1
        return task

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve specific task from collection by ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Task object if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Modify existing task properties.

        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            True if task was updated, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.update(title, description)
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """
        Remove task from collection by ID.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if task was deleted, False if task not found
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                return True
        return False

    def list_tasks(self, status: str = "all") -> List[Task]:
        """
        Return all tasks or filtered subset.

        Args:
            status: Filter by status ('all', 'pending', 'completed')

        Returns:
            List of Task objects matching the filter
        """
        if status == "pending":
            return [task for task in self.tasks if not task.completed]
        elif status == "completed":
            return [task for task in self.tasks if task.completed]
        else:  # all
            return self.tasks.copy()

    def toggle_completion(self, task_id: int) -> bool:
        """
        Change completed status of specific task.

        Args:
            task_id: ID of the task to toggle

        Returns:
            True if task status was toggled, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.completed = not task.completed
            return True
        return False

    def mark_task_complete(self, task_id: int) -> bool:
        """
        Mark a specific task as complete.

        Args:
            task_id: ID of the task to mark complete

        Returns:
            True if task was marked complete, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.completed = True
            return True
        return False

    def mark_task_incomplete(self, task_id: int) -> bool:
        """
        Mark a specific task as incomplete.

        Args:
            task_id: ID of the task to mark incomplete

        Returns:
            True if task was marked incomplete, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.completed = False
            return True
        return False