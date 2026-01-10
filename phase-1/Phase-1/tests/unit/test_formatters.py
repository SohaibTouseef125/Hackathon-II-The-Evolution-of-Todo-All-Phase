"""Unit tests for CLI formatters."""

import pytest
from datetime import date, time, timedelta

from src.models.task import Task, Priority, Recurrence
from src.services.task_store import TaskStore
from src.services.task_service import TaskService
from src.cli.formatters import (
    format_task,
    format_task_list,
    format_task_created,
    format_task_updated,
    format_task_completed,
    format_search_results,
    format_filter_results,
    format_reminder_list,
    format_config,
    format_error,
)


class TestFormatTask:
    """Tests for format_task function."""

    def test_format_basic_task(self):
        """Format task with basic fields."""
        task = Task(id=1, title="Test Task")
        result = format_task(task)

        assert "1." in result
        assert "[MEDIUM]" in result
        assert "[ ]" in result
        assert "Test Task" in result

    def test_format_completed_task(self):
        """Format completed task shows [x]."""
        task = Task(id=1, title="Done", completed=True)
        result = format_task(task)

        assert "[x]" in result

    def test_format_high_priority(self):
        """Format high priority task shows [HIGH]."""
        task = Task(id=1, title="Urgent", priority=Priority.HIGH)
        result = format_task(task)

        assert "[HIGH]" in result

    def test_format_with_tags(self):
        """Format task with tags."""
        task = Task(id=1, title="Tagged", tags=["work", "urgent"])
        result = format_task(task)

        assert "[tags: work, urgent]" in result

    def test_format_with_due_date(self):
        """Format task with due date."""
        task = Task(id=1, title="Due", due_date=date(2025, 1, 15))
        result = format_task(task)

        assert "[due: 2025-01-15]" in result

    def test_format_with_due_time(self):
        """Format task with due date and time."""
        task = Task(
            id=1,
            title="Meeting",
            due_date=date(2025, 1, 15),
            due_time=time(14, 30)
        )
        result = format_task(task)

        assert "[due: 2025-01-15 14:30]" in result

    def test_format_recurring_task(self):
        """Format recurring task shows pattern."""
        task = Task(
            id=1,
            title="Standup",
            due_date=date(2025, 1, 15),
            recurrence=Recurrence.DAILY
        )
        result = format_task(task)

        assert "(repeats: daily)" in result

    def test_format_without_id(self):
        """Format task without ID."""
        task = Task(id=1, title="No ID")
        result = format_task(task, show_id=False)

        assert "1." not in result
        assert "No ID" in result


class TestFormatTaskWithService:
    """Tests for format_task with service for status indicators."""

    @pytest.fixture
    def service(self):
        """Create service for testing."""
        store = TaskStore()
        return TaskService(store)

    def test_format_overdue_task(self, service):
        """Format overdue task shows [OVERDUE]."""
        task = Task(
            id=1,
            title="Late",
            due_date=date.today() - timedelta(days=1)
        )
        result = format_task(task, service=service)

        assert "[OVERDUE]" in result

    def test_format_reminder_task(self, service):
        """Format task due soon shows [REMINDER]."""
        # Task due in 12 hours (within default 24h threshold)
        task = Task(
            id=1,
            title="Soon",
            due_date=date.today(),
            due_time=time(23, 59)
        )
        result = format_task(task, service=service)

        # Should show REMINDER (if not already past)
        # This depends on current time, so we check for either
        assert "[REMINDER]" in result or "[OVERDUE]" in result


class TestFormatMessages:
    """Tests for message formatting functions."""

    def test_format_task_created(self):
        """Format task creation message."""
        task = Task(id=1, title="New Task", priority=Priority.HIGH)
        result = format_task_created(task)

        assert "Task 1 created:" in result
        assert "[HIGH]" in result
        assert "New Task" in result

    def test_format_task_updated(self):
        """Format task update message."""
        task = Task(id=1, title="Updated Task")
        result = format_task_updated(task)

        assert "Task 1 updated:" in result
        assert "Updated Task" in result

    def test_format_task_completed_basic(self):
        """Format task completion message (non-recurring)."""
        task = Task(id=1, title="Done", completed=True)
        result = format_task_completed(task)

        assert "Task 1 completed:" in result
        assert "New recurring task" not in result

    def test_format_task_completed_recurring(self):
        """Format task completion message with new recurring task."""
        task = Task(id=1, title="Standup", completed=True)
        new_task = Task(
            id=2,
            title="Standup",
            due_date=date(2025, 1, 16),
            recurrence=Recurrence.DAILY
        )
        result = format_task_completed(task, new_task)

        assert "Task 1 completed:" in result
        assert "New recurring task created:" in result
        assert "Task 2:" in result


class TestFormatResults:
    """Tests for result list formatting functions."""

    def test_format_search_results_empty(self):
        """Format empty search results."""
        result = format_search_results([], "test")
        assert "No tasks found matching 'test'" in result

    def test_format_search_results_found(self):
        """Format search results with matches."""
        tasks = [Task(id=1, title="Test Task")]
        result = format_search_results(tasks, "test")

        assert "Found 1 tasks matching 'test'" in result
        assert "Test Task" in result

    def test_format_filter_results_empty(self):
        """Format empty filter results."""
        result = format_filter_results([])
        assert "No tasks match the specified filters" in result

    def test_format_filter_results_with_filters(self):
        """Format filter results with header."""
        tasks = [Task(id=1, title="Test")]
        result = format_filter_results(tasks, status="pending", priority="high")

        assert "Pending high-priority tasks" in result


class TestFormatConfig:
    """Tests for configuration formatting."""

    def test_format_config(self):
        """Format configuration display."""
        settings = {"reminder_threshold": "24h"}
        result = format_config(settings)

        assert "Current settings:" in result
        assert "reminder_threshold: 24h" in result


class TestFormatError:
    """Tests for error formatting."""

    def test_format_error(self):
        """Format error message."""
        result = format_error("Something went wrong")
        assert result == "Error: Something went wrong"
