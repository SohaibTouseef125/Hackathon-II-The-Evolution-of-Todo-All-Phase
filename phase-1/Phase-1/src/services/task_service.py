"""Business logic service for task operations.

This module provides the TaskService class for task validation and operations.
"""

import re
from datetime import datetime, date, time, timedelta
from typing import List, Optional, Tuple

from src.models.task import Task, Priority, Recurrence
from src.models.config import get_config
from src.services.task_store import TaskStore
from src.services.recurrence import calculate_next_due_date


class TaskService:
    """Business logic for task operations.

    Provides validation, search, filter, and sort functionality.
    """

    # Validation constants
    MAX_TITLE_LENGTH = 200
    MAX_DESCRIPTION_LENGTH = 1000
    MAX_TAGS = 10
    MAX_TAG_LENGTH = 50
    TAG_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")

    def __init__(self, store: TaskStore):
        """Initialize service with task store.

        Args:
            store: TaskStore instance for data persistence
        """
        self.store = store

    # ==================== Validation ====================

    def validate_title(self, title: str) -> str:
        """Validate and normalize task title.

        Args:
            title: Raw title string

        Returns:
            Trimmed title string

        Raises:
            ValueError: If title is empty or too long
        """
        if not title:
            raise ValueError("Task title is required")

        title = title.strip()

        if not title:
            raise ValueError("Task title is required")

        if len(title) > self.MAX_TITLE_LENGTH:
            raise ValueError(
                f"Task title must be {self.MAX_TITLE_LENGTH} characters or less"
            )

        return title

    def validate_description(self, description: Optional[str]) -> Optional[str]:
        """Validate and normalize task description.

        Args:
            description: Raw description string or None

        Returns:
            Trimmed description string or None

        Raises:
            ValueError: If description is too long
        """
        if not description:
            return None

        description = description.strip()

        if not description:
            return None

        if len(description) > self.MAX_DESCRIPTION_LENGTH:
            raise ValueError(
                f"Task description must be {self.MAX_DESCRIPTION_LENGTH} characters or less"
            )

        return description

    def validate_priority(self, priority_str: str) -> Priority:
        """Validate and parse priority string.

        Args:
            priority_str: Priority as string (high, medium, low)

        Returns:
            Priority enum value

        Raises:
            ValueError: If invalid priority
        """
        try:
            return Priority.from_string(priority_str)
        except ValueError:
            raise ValueError("Invalid priority. Use: high, medium, low")

    def validate_tags(self, tags_str: str) -> List[str]:
        """Validate and parse tags from comma-separated string.

        Args:
            tags_str: Comma-separated tags string

        Returns:
            List of normalized, deduplicated tags

        Raises:
            ValueError: If tags are invalid
        """
        if not tags_str or not tags_str.strip():
            return []

        tags = []
        seen = set()

        for tag in tags_str.split(","):
            tag = tag.strip().lower()

            if not tag:
                continue

            if not self.TAG_PATTERN.match(tag):
                raise ValueError(
                    "Invalid tag format. Tags must be alphanumeric with hyphens/underscores, max 50 chars"
                )

            if len(tag) > self.MAX_TAG_LENGTH:
                raise ValueError(
                    f"Invalid tag format. Tags must be alphanumeric with hyphens/underscores, max {self.MAX_TAG_LENGTH} chars"
                )

            if tag not in seen:
                tags.append(tag)
                seen.add(tag)

        if len(tags) > self.MAX_TAGS:
            raise ValueError(f"Maximum {self.MAX_TAGS} tags allowed")

        return tags

    def validate_due_date(self, date_str: str) -> Optional[date]:
        """Validate and parse due date string.

        Args:
            date_str: Date in YYYY-MM-DD format or "none"

        Returns:
            date object or None

        Raises:
            ValueError: If date format invalid or in the past
        """
        if not date_str or date_str.lower() == "none":
            return None

        try:
            d = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

        if d < date.today():
            raise ValueError("Due date cannot be in the past")

        return d

    def validate_due_time(
        self, time_str: str, has_due_date: bool
    ) -> Optional[time]:
        """Validate and parse due time string.

        Args:
            time_str: Time in HH:MM format or None
            has_due_date: Whether task has a due date

        Returns:
            time object or None

        Raises:
            ValueError: If time format invalid or missing due date
        """
        if not time_str:
            return None

        if not has_due_date:
            raise ValueError(
                "Due time requires a due date. Use --due YYYY-MM-DD --time HH:MM"
            )

        try:
            return datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            raise ValueError("Invalid time format. Use HH:MM (24-hour)")

    def validate_recurrence(
        self, recurrence_str: str, has_due_date: bool
    ) -> Recurrence:
        """Validate and parse recurrence pattern.

        Args:
            recurrence_str: Recurrence pattern string
            has_due_date: Whether task has a due date

        Returns:
            Recurrence enum value

        Raises:
            ValueError: If invalid or missing due date for recurring task
        """
        try:
            recurrence = Recurrence.from_string(recurrence_str)
        except ValueError:
            raise ValueError(
                "Invalid recurrence. Use: daily, weekly, monthly, none"
            )

        if recurrence != Recurrence.NONE and not has_due_date:
            raise ValueError(
                "Recurring tasks must have a due date. Use --due YYYY-MM-DD"
            )

        return recurrence

    # ==================== CRUD Operations ====================

    def create_task(
        self,
        title: str,
        description: Optional[str] = None,
        priority: Priority = Priority.MEDIUM,
        tags: Optional[List[str]] = None,
        due_date: Optional[date] = None,
        due_time: Optional[time] = None,
        recurrence: Recurrence = Recurrence.NONE,
    ) -> Task:
        """Create a new task with validation.

        Args:
            title: Task title (required)
            description: Optional description
            priority: Priority level (default: MEDIUM)
            tags: List of tags (default: empty)
            due_date: Optional due date
            due_time: Optional due time
            recurrence: Recurrence pattern (default: NONE)

        Returns:
            Created task

        Raises:
            ValueError: If validation fails
        """
        title = self.validate_title(title)
        description = self.validate_description(description)

        task = Task(
            id=0,  # Will be assigned by store
            title=title,
            description=description,
            priority=priority,
            tags=tags or [],
            due_date=due_date,
            due_time=due_time,
            recurrence=recurrence,
        )

        return self.store.add(task)

    def get_task(self, task_id: int) -> Task:
        """Get task by ID.

        Args:
            task_id: Task ID

        Returns:
            Task object

        Raises:
            ValueError: If task not found
        """
        task = self.store.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        return task

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Priority] = None,
        tags: Optional[List[str]] = None,
        due_date=None,
        due_time=None,
        recurrence: Optional[Recurrence] = None,
    ) -> Task:
        """Update task fields.

        Args:
            task_id: Task ID to update
            title: New title (if provided)
            description: New description (if provided)
            priority: New priority (if provided)
            tags: New tags (if provided)
            due_date: New due date (if provided, use "none" to clear)
            due_time: New due time (if provided, use "none" to clear)
            recurrence: New recurrence (if provided)

        Returns:
            Updated task

        Raises:
            ValueError: If task not found or validation fails
        """
        task = self.store.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        if title is not None:
            title = self.validate_title(title)

        if description is not None:
            description = self.validate_description(description)

        updated = self.store.update(
            task_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            due_date=due_date,
            due_time=due_time,
            recurrence=recurrence,
        )

        return updated

    def delete_task(self, task_id: int) -> bool:
        """Delete task by ID.

        Args:
            task_id: Task ID to delete

        Returns:
            True if deleted

        Raises:
            ValueError: If task not found
        """
        if not self.store.delete(task_id):
            raise ValueError(f"Task {task_id} not found")
        return True

    def complete_task(self, task_id: int) -> Tuple[Task, Optional[Task]]:
        """Mark task as complete, creating next occurrence if recurring.

        Args:
            task_id: Task ID to complete

        Returns:
            Tuple of (completed_task, new_recurring_task or None)

        Raises:
            ValueError: If task not found
        """
        task = self.store.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        # Mark as complete
        self.store.update(task_id, completed=True)

        # Create next occurrence if recurring
        new_task = None
        if task.recurrence != Recurrence.NONE and task.due_date:
            next_due = calculate_next_due_date(task.due_date, task.recurrence)

            new_task = Task(
                id=0,
                title=task.title,
                description=task.description,
                priority=task.priority,
                tags=task.tags.copy(),
                due_date=next_due,
                due_time=task.due_time,
                recurrence=task.recurrence,
            )
            new_task = self.store.add(new_task)

        return task, new_task

    def uncomplete_task(self, task_id: int) -> Task:
        """Mark task as not complete.

        Args:
            task_id: Task ID

        Returns:
            Updated task

        Raises:
            ValueError: If task not found
        """
        task = self.store.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        return self.store.update(task_id, completed=False)

    # ==================== Search ====================

    def search_tasks(self, keyword: str) -> List[Task]:
        """Search tasks by keyword in title and description.

        Args:
            keyword: Search keyword (case-insensitive)

        Returns:
            List of matching tasks
        """
        if not keyword or not keyword.strip():
            return []

        keyword_lower = keyword.strip().lower()
        tasks = self.store.list_all()

        return [
            task
            for task in tasks
            if keyword_lower in task.title.lower()
            or (task.description and keyword_lower in task.description.lower())
        ]

    # ==================== Filter ====================

    def filter_tasks(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        due: Optional[str] = None,
    ) -> List[Task]:
        """Filter tasks by status, priority, and due date.

        Args:
            status: Filter by status (all, pending, completed)
            priority: Filter by priority (all, high, medium, low)
            due: Filter by due date (all, today, week, overdue)

        Returns:
            List of matching tasks
        """
        tasks = self.store.list_all()

        # Filter by status
        if status and status != "all":
            if status == "pending":
                tasks = [t for t in tasks if not t.completed]
            elif status == "completed":
                tasks = [t for t in tasks if t.completed]

        # Filter by priority
        if priority and priority != "all":
            tasks = [t for t in tasks if t.priority.value == priority]

        # Filter by due date
        if due and due != "all":
            today = date.today()

            if due == "today":
                tasks = [t for t in tasks if t.due_date == today]
            elif due == "week":
                week_end = today + timedelta(days=7)
                tasks = [
                    t for t in tasks
                    if t.due_date and t.due_date <= week_end
                ]
            elif due == "overdue":
                tasks = [t for t in tasks if self._is_overdue(t)]

        return tasks

    # ==================== Sort ====================

    def sort_tasks(
        self,
        tasks: List[Task],
        sort_by: str = "created",
        reverse: bool = False,
    ) -> List[Task]:
        """Sort tasks by specified field.

        Args:
            tasks: List of tasks to sort
            sort_by: Sort field (created, due_date, priority, title)
            reverse: Whether to reverse sort order

        Returns:
            Sorted list of tasks
        """
        if sort_by == "due_date":
            # None values go to end
            sentinel = date.max if not reverse else date.min
            return sorted(
                tasks,
                key=lambda t: t.due_date or sentinel,
                reverse=reverse,
            )
        elif sort_by == "priority":
            return sorted(
                tasks,
                key=lambda t: t.priority.sort_key(),
                reverse=reverse,
            )
        elif sort_by == "title":
            return sorted(
                tasks,
                key=lambda t: t.title.lower(),
                reverse=reverse,
            )
        else:  # created
            return sorted(
                tasks,
                key=lambda t: t.created_at,
                reverse=reverse,
            )

    # ==================== Reminders ====================

    def get_reminder_tasks(self) -> List[Task]:
        """Get tasks that are overdue or due within threshold.

        Returns:
            List of tasks needing attention
        """
        tasks = self.store.list_all()
        return [
            t for t in tasks
            if not t.completed and (self._is_overdue(t) or self._is_reminder(t))
        ]

    def _is_overdue(self, task: Task) -> bool:
        """Check if task is overdue.

        Args:
            task: Task to check

        Returns:
            True if task is past due
        """
        if task.completed or not task.due_date:
            return False

        due_datetime = self._get_due_datetime(task)
        return due_datetime < datetime.now()

    def _is_reminder(self, task: Task) -> bool:
        """Check if task is due within reminder threshold.

        Args:
            task: Task to check

        Returns:
            True if task is due soon
        """
        if task.completed or not task.due_date:
            return False

        if self._is_overdue(task):
            return False

        due_datetime = self._get_due_datetime(task)
        config = get_config()
        threshold_end = datetime.now() + config.reminder_threshold

        return datetime.now() <= due_datetime <= threshold_end

    def _get_due_datetime(self, task: Task) -> datetime:
        """Get task due date/time as datetime.

        Args:
            task: Task with due date

        Returns:
            datetime combining due_date and due_time
        """
        if task.due_time:
            return datetime.combine(task.due_date, task.due_time)
        return datetime.combine(task.due_date, time(23, 59, 59))

    def is_overdue(self, task: Task) -> bool:
        """Public method to check if task is overdue."""
        return self._is_overdue(task)

    def is_reminder(self, task: Task) -> bool:
        """Public method to check if task is in reminder window."""
        return self._is_reminder(task)
