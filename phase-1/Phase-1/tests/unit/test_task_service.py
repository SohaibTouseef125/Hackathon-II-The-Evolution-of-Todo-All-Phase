"""Unit tests for TaskService.

Tests for validation, CRUD, search, filter, sort, and reminder functionality.
"""

import pytest
from datetime import date, time, timedelta, datetime

from src.models.task import Task, Priority, Recurrence
from src.services.task_store import TaskStore
from src.services.task_service import TaskService


class TestTaskServiceValidation:
    """Tests for TaskService validation methods."""

    @pytest.fixture
    def service(self):
        """Create fresh service for each test."""
        store = TaskStore()
        return TaskService(store)

    # ==================== Title Validation ====================

    def test_validate_title_success(self, service):
        """Valid title should pass validation."""
        result = service.validate_title("Valid Title")
        assert result == "Valid Title"

    def test_validate_title_trims_whitespace(self, service):
        """Title should be trimmed."""
        result = service.validate_title("  Trimmed  ")
        assert result == "Trimmed"

    def test_validate_title_empty_raises(self, service):
        """Empty title should raise ValueError."""
        with pytest.raises(ValueError, match="required"):
            service.validate_title("")

    def test_validate_title_whitespace_only_raises(self, service):
        """Whitespace-only title should raise ValueError."""
        with pytest.raises(ValueError, match="required"):
            service.validate_title("   ")

    def test_validate_title_too_long_raises(self, service):
        """Title over 200 chars should raise ValueError."""
        long_title = "x" * 201
        with pytest.raises(ValueError, match="200 characters"):
            service.validate_title(long_title)

    # ==================== Description Validation ====================

    def test_validate_description_success(self, service):
        """Valid description should pass validation."""
        result = service.validate_description("Valid description")
        assert result == "Valid description"

    def test_validate_description_none_returns_none(self, service):
        """None description should return None."""
        result = service.validate_description(None)
        assert result is None

    def test_validate_description_empty_returns_none(self, service):
        """Empty description should return None."""
        result = service.validate_description("")
        assert result is None

    def test_validate_description_too_long_raises(self, service):
        """Description over 1000 chars should raise ValueError."""
        long_desc = "x" * 1001
        with pytest.raises(ValueError, match="1000 characters"):
            service.validate_description(long_desc)

    # ==================== Priority Validation ====================

    def test_validate_priority_high(self, service):
        """'high' should return Priority.HIGH."""
        result = service.validate_priority("high")
        assert result == Priority.HIGH

    def test_validate_priority_case_insensitive(self, service):
        """Priority validation should be case-insensitive."""
        assert service.validate_priority("HIGH") == Priority.HIGH
        assert service.validate_priority("Medium") == Priority.MEDIUM

    def test_validate_priority_invalid_raises(self, service):
        """Invalid priority should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid priority"):
            service.validate_priority("urgent")

    # ==================== Tags Validation ====================

    def test_validate_tags_success(self, service):
        """Valid tags should pass validation."""
        result = service.validate_tags("work,home,urgent")
        assert result == ["work", "home", "urgent"]

    def test_validate_tags_lowercased(self, service):
        """Tags should be lowercased."""
        result = service.validate_tags("Work,HOME,Urgent")
        assert result == ["work", "home", "urgent"]

    def test_validate_tags_deduplicated(self, service):
        """Duplicate tags should be removed."""
        result = service.validate_tags("work,work,home")
        assert result == ["work", "home"]

    def test_validate_tags_empty_returns_empty(self, service):
        """Empty tags string should return empty list."""
        result = service.validate_tags("")
        assert result == []

    def test_validate_tags_max_10(self, service):
        """More than 10 tags should raise ValueError."""
        tags = ",".join([f"tag{i}" for i in range(11)])
        with pytest.raises(ValueError, match="Maximum 10 tags"):
            service.validate_tags(tags)

    def test_validate_tags_invalid_format_raises(self, service):
        """Tags with special characters should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid tag format"):
            service.validate_tags("work@home")

    def test_validate_tags_allows_hyphens_underscores(self, service):
        """Tags with hyphens and underscores should pass."""
        result = service.validate_tags("work-related,home_tasks")
        assert result == ["work-related", "home_tasks"]

    # ==================== Due Date Validation ====================

    def test_validate_due_date_success(self, service):
        """Valid future date should pass validation."""
        future = (date.today() + timedelta(days=7)).isoformat()
        result = service.validate_due_date(future)
        assert result == date.today() + timedelta(days=7)

    def test_validate_due_date_today_passes(self, service):
        """Today's date should pass validation."""
        result = service.validate_due_date(date.today().isoformat())
        assert result == date.today()

    def test_validate_due_date_none_string(self, service):
        """'none' should return None."""
        result = service.validate_due_date("none")
        assert result is None

    def test_validate_due_date_past_raises(self, service):
        """Past date should raise ValueError."""
        past = (date.today() - timedelta(days=1)).isoformat()
        with pytest.raises(ValueError, match="cannot be in the past"):
            service.validate_due_date(past)

    def test_validate_due_date_invalid_format_raises(self, service):
        """Invalid date format should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid date format"):
            service.validate_due_date("01-15-2025")

    # ==================== Due Time Validation ====================

    def test_validate_due_time_success(self, service):
        """Valid time with due date should pass."""
        result = service.validate_due_time("14:30", has_due_date=True)
        assert result == time(14, 30)

    def test_validate_due_time_without_date_raises(self, service):
        """Time without due date should raise ValueError."""
        with pytest.raises(ValueError, match="requires a due date"):
            service.validate_due_time("14:30", has_due_date=False)

    def test_validate_due_time_invalid_format_raises(self, service):
        """Invalid time format should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid time format"):
            service.validate_due_time("2:30pm", has_due_date=True)

    # ==================== Recurrence Validation ====================

    def test_validate_recurrence_success(self, service):
        """Valid recurrence with due date should pass."""
        result = service.validate_recurrence("daily", has_due_date=True)
        assert result == Recurrence.DAILY

    def test_validate_recurrence_none_without_date(self, service):
        """'none' recurrence without due date should pass."""
        result = service.validate_recurrence("none", has_due_date=False)
        assert result == Recurrence.NONE

    def test_validate_recurrence_without_date_raises(self, service):
        """Recurring task without due date should raise ValueError."""
        with pytest.raises(ValueError, match="must have a due date"):
            service.validate_recurrence("daily", has_due_date=False)


class TestTaskServiceCRUD:
    """Tests for TaskService CRUD operations."""

    @pytest.fixture
    def service(self):
        """Create fresh service for each test."""
        store = TaskStore()
        return TaskService(store)

    def test_create_task_basic(self, service):
        """Create task with basic fields."""
        task = service.create_task(title="Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.priority == Priority.MEDIUM
        assert task.tags == []

    def test_create_task_full(self, service):
        """Create task with all fields."""
        due = date.today() + timedelta(days=7)

        task = service.create_task(
            title="Full Task",
            description="Description",
            priority=Priority.HIGH,
            tags=["work", "urgent"],
            due_date=due,
            due_time=time(14, 30),
            recurrence=Recurrence.DAILY,
        )

        assert task.title == "Full Task"
        assert task.description == "Description"
        assert task.priority == Priority.HIGH
        assert task.tags == ["work", "urgent"]
        assert task.due_date == due
        assert task.due_time == time(14, 30)
        assert task.recurrence == Recurrence.DAILY

    def test_get_task_success(self, service):
        """Get existing task."""
        created = service.create_task(title="Test")
        task = service.get_task(created.id)

        assert task.id == created.id

    def test_get_task_not_found_raises(self, service):
        """Get non-existent task raises ValueError."""
        with pytest.raises(ValueError, match="not found"):
            service.get_task(999)

    def test_update_task_title(self, service):
        """Update task title."""
        created = service.create_task(title="Original")
        updated = service.update_task(created.id, title="Updated")

        assert updated.title == "Updated"

    def test_delete_task_success(self, service):
        """Delete existing task."""
        created = service.create_task(title="Test")
        result = service.delete_task(created.id)

        assert result is True

        with pytest.raises(ValueError):
            service.get_task(created.id)


class TestTaskServiceSearch:
    """Tests for TaskService search functionality."""

    @pytest.fixture
    def service(self):
        """Create service with sample tasks."""
        store = TaskStore()
        service = TaskService(store)

        service.create_task(title="Buy groceries", description="Milk and bread")
        service.create_task(title="Finish report", description="Q4 report")
        service.create_task(title="Call mom")

        return service

    def test_search_matches_title(self, service):
        """Search should match title."""
        results = service.search_tasks("groceries")
        assert len(results) == 1
        assert results[0].title == "Buy groceries"

    def test_search_matches_description(self, service):
        """Search should match description."""
        results = service.search_tasks("Q4")
        assert len(results) == 1
        assert results[0].title == "Finish report"

    def test_search_case_insensitive(self, service):
        """Search should be case-insensitive."""
        results = service.search_tasks("GROCERIES")
        assert len(results) == 1

    def test_search_partial_match(self, service):
        """Search should match partial strings."""
        results = service.search_tasks("report")
        assert len(results) == 1

    def test_search_no_results(self, service):
        """Search with no matches returns empty list."""
        results = service.search_tasks("xyz")
        assert len(results) == 0


class TestTaskServiceFilter:
    """Tests for TaskService filter functionality."""

    @pytest.fixture
    def service(self):
        """Create service with sample tasks."""
        store = TaskStore()
        service = TaskService(store)

        # Create varied tasks
        t1 = service.create_task(title="High priority", priority=Priority.HIGH)
        t2 = service.create_task(title="Low priority", priority=Priority.LOW)
        t3 = service.create_task(title="With due date", due_date=date.today())

        # Complete one task
        service.complete_task(t1.id)

        return service

    def test_filter_by_status_pending(self, service):
        """Filter pending tasks."""
        results = service.filter_tasks(status="pending")
        assert len(results) == 2
        assert all(not t.completed for t in results)

    def test_filter_by_status_completed(self, service):
        """Filter completed tasks."""
        results = service.filter_tasks(status="completed")
        assert len(results) == 1
        assert all(t.completed for t in results)

    def test_filter_by_priority(self, service):
        """Filter by priority."""
        results = service.filter_tasks(priority="low")
        assert len(results) == 1
        assert results[0].priority == Priority.LOW

    def test_filter_by_due_today(self, service):
        """Filter tasks due today."""
        results = service.filter_tasks(due="today")
        assert len(results) == 1

    def test_filter_combined(self, service):
        """Combined filters work correctly."""
        results = service.filter_tasks(status="pending", priority="low")
        assert len(results) == 1


class TestTaskServiceSort:
    """Tests for TaskService sort functionality."""

    @pytest.fixture
    def service(self):
        """Create service with sample tasks."""
        store = TaskStore()
        service = TaskService(store)

        service.create_task(title="Zebra", priority=Priority.LOW)
        service.create_task(title="Apple", priority=Priority.HIGH)
        service.create_task(
            title="Middle",
            priority=Priority.MEDIUM,
            due_date=date.today() + timedelta(days=1),
        )

        return service

    def test_sort_by_title(self, service):
        """Sort alphabetically by title."""
        tasks = service.store.list_all()
        sorted_tasks = service.sort_tasks(tasks, sort_by="title")

        assert sorted_tasks[0].title == "Apple"
        assert sorted_tasks[1].title == "Middle"
        assert sorted_tasks[2].title == "Zebra"

    def test_sort_by_title_reverse(self, service):
        """Sort alphabetically by title reversed."""
        tasks = service.store.list_all()
        sorted_tasks = service.sort_tasks(tasks, sort_by="title", reverse=True)

        assert sorted_tasks[0].title == "Zebra"

    def test_sort_by_priority(self, service):
        """Sort by priority (high first)."""
        tasks = service.store.list_all()
        sorted_tasks = service.sort_tasks(tasks, sort_by="priority")

        assert sorted_tasks[0].priority == Priority.HIGH
        assert sorted_tasks[1].priority == Priority.MEDIUM
        assert sorted_tasks[2].priority == Priority.LOW

    def test_sort_by_due_date_nulls_at_end(self, service):
        """Tasks without due date should sort to end."""
        tasks = service.store.list_all()
        sorted_tasks = service.sort_tasks(tasks, sort_by="due_date")

        # Only "Middle" has a due date, should be first
        assert sorted_tasks[0].title == "Middle"
        assert sorted_tasks[0].due_date is not None
        # Others should be at end
        assert sorted_tasks[1].due_date is None
        assert sorted_tasks[2].due_date is None


class TestTaskServiceComplete:
    """Tests for TaskService complete/recurrence functionality."""

    @pytest.fixture
    def service(self):
        """Create fresh service."""
        store = TaskStore()
        return TaskService(store)

    def test_complete_task_basic(self, service):
        """Complete non-recurring task."""
        task = service.create_task(title="One-time")
        completed, new_task = service.complete_task(task.id)

        assert completed.completed is True
        assert new_task is None

    def test_complete_recurring_creates_new(self, service):
        """Complete recurring task creates new occurrence."""
        due = date.today()
        task = service.create_task(
            title="Daily standup",
            due_date=due,
            recurrence=Recurrence.DAILY,
            priority=Priority.HIGH,
            tags=["work"],
        )

        completed, new_task = service.complete_task(task.id)

        assert completed.completed is True
        assert new_task is not None
        assert new_task.id != task.id
        assert new_task.title == "Daily standup"
        assert new_task.due_date == due + timedelta(days=1)
        assert new_task.priority == Priority.HIGH
        assert new_task.tags == ["work"]
        assert new_task.completed is False
