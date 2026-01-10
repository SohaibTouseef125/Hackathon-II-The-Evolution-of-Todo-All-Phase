"""In-memory task storage with CRUD operations.

This module provides the TaskStore class for storing and managing tasks.
"""

from datetime import datetime
from typing import Dict, List, Optional

from src.models.task import Task, Priority, Recurrence


class TaskStore:
    """In-memory task storage with CRUD operations.

    Attributes:
        _tasks: Dictionary mapping task IDs to Task objects
        _next_id: Next available ID for new tasks
    """

    def __init__(self):
        """Initialize empty task store."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task: Task) -> Task:
        """Add a new task to the store.

        The task's ID will be assigned automatically.

        Args:
            task: Task object to add (id will be overwritten)

        Returns:
            The created task with assigned ID
        """
        task.id = self._next_id
        task.created_at = datetime.now()
        task.updated_at = datetime.now()
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Optional[Task]:
        """Get a task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            Task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def update(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None,
        priority: Optional[Priority] = None,
        tags: Optional[List[str]] = None,
        due_date=None,  # Can be date or "none" sentinel
        due_time=None,  # Can be time or "none" sentinel
        recurrence: Optional[Recurrence] = None,
    ) -> Optional[Task]:
        """Update a task's fields.

        Only provided fields are updated. Use special sentinel values to clear fields.

        Args:
            task_id: The ID of the task to update
            title: New title (if provided)
            description: New description (if provided)
            completed: New completion status (if provided)
            priority: New priority (if provided)
            tags: New tags list (if provided)
            due_date: New due date (if provided)
            due_time: New due time (if provided)
            recurrence: New recurrence pattern (if provided)

        Returns:
            Updated task if found, None otherwise
        """
        task = self._tasks.get(task_id)
        if not task:
            return None

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description if description else None
        if completed is not None:
            task.completed = completed
        if priority is not None:
            task.priority = priority
        if tags is not None:
            task.tags = tags
        if due_date is not None:
            # Handle "none" sentinel to clear due_date
            task.due_date = None if due_date == "none" else due_date
        if due_time is not None:
            task.due_time = None if due_time == "none" else due_time
        if recurrence is not None:
            task.recurrence = recurrence

        task.updated_at = datetime.now()
        return task

    def delete(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if deleted, False if not found
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def list_all(self) -> List[Task]:
        """Get all tasks in the store.

        Returns:
            List of all tasks, ordered by ID
        """
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def count(self) -> int:
        """Get the number of tasks in the store.

        Returns:
            Number of tasks
        """
        return len(self._tasks)

    def clear(self) -> None:
        """Remove all tasks and reset ID counter."""
        self._tasks.clear()
        self._next_id = 1


# Global store instance
_store: TaskStore | None = None


def get_store() -> TaskStore:
    """Get or create the global store instance.

    Returns:
        Global TaskStore instance
    """
    global _store
    if _store is None:
        _store = TaskStore()
    return _store


def reset_store() -> None:
    """Reset store to empty (useful for testing)."""
    global _store
    _store = None
