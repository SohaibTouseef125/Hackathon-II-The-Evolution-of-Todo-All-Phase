"""
TaskService for business logic of task operations.

This module contains the TaskService class which handles all business logic
for task operations, including validation, error handling, and interaction
with the data models.

The service layer provides a clean interface between the CLI layer and the
data models, implementing all business rules and validation requirements.
"""
from typing import Optional
from .models import TaskList, Task


class TaskService:
    """
    Business logic layer for task operations.
    """
    def __init__(self):
        """Initialize the TaskService with an in-memory TaskList."""
        self.task_list = TaskList()

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task with title and optional description.

        Args:
            title: Title of the task (required, 1-200 characters)
            description: Optional description of the task (max 1000 characters)

        Returns:
            The newly created Task object

        Raises:
            ValueError: If title validation fails or max task limit is reached
        """
        return self.task_list.add_task(title, description)

    def list_tasks(self, status: str = "all") -> list:
        """
        Get all tasks or filtered by status.

        Args:
            status: Filter by status ('all', 'pending', 'completed')

        Returns:
            List of Task objects matching the filter
        """
        return self.task_list.list_tasks(status)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update existing task details.

        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            True if task was updated, False if task not found
        """
        return self.task_list.update_task(task_id, title, description)

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its unique identifier.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if task was deleted, False if task not found
        """
        return self.task_list.delete_task(task_id)

    def mark_task_complete(self, task_id: int) -> bool:
        """
        Mark a task as complete by its unique identifier.

        Args:
            task_id: ID of the task to mark complete

        Returns:
            True if task was marked complete, False if task not found
        """
        return self.task_list.mark_task_complete(task_id)

    def mark_task_incomplete(self, task_id: int) -> bool:
        """
        Mark a task as incomplete by its unique identifier.

        Args:
            task_id: ID of the task to mark incomplete

        Returns:
            True if task was marked incomplete, False if task not found
        """
        return self.task_list.mark_task_incomplete(task_id)

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a specific task by its ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Task object if found, None otherwise
        """
        return self.task_list.get_task_by_id(task_id)