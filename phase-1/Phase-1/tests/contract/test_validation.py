"""Contract tests for input validation.

These tests verify that all validation rules match the specification.
"""

import pytest
from datetime import date, timedelta

from src.services.task_store import TaskStore
from src.services.task_service import TaskService
from src.models.config import Config


class TestTitleValidation:
    """Contract tests for title validation (FR-T requirements)."""

    @pytest.fixture
    def service(self):
        """Create service for testing."""
        store = TaskStore()
        return TaskService(store)

    def test_title_required(self, service):
        """Title is required - empty string rejected."""
        with pytest.raises(ValueError) as exc:
            service.validate_title("")
        assert "required" in str(exc.value).lower()

    def test_title_whitespace_only_rejected(self, service):
        """Title of only whitespace rejected."""
        with pytest.raises(ValueError) as exc:
            service.validate_title("   ")
        assert "required" in str(exc.value).lower()

    def test_title_max_200_chars(self, service):
        """Title max 200 characters after trimming."""
        # Exactly 200 should pass
        title_200 = "x" * 200
        result = service.validate_title(title_200)
        assert len(result) == 200

        # 201 should fail
        with pytest.raises(ValueError) as exc:
            service.validate_title("x" * 201)
        assert "200 characters" in str(exc.value)

    def test_title_trimmed(self, service):
        """Title trimmed of leading/trailing whitespace."""
        result = service.validate_title("  Hello  ")
        assert result == "Hello"


class TestDescriptionValidation:
    """Contract tests for description validation."""

    @pytest.fixture
    def service(self):
        """Create service for testing."""
        store = TaskStore()
        return TaskService(store)

    def test_description_optional(self, service):
        """Description is optional - None returns None."""
        assert service.validate_description(None) is None
        assert service.validate_description("") is None

    def test_description_max_1000_chars(self, service):
        """Description max 1000 characters."""
        # Exactly 1000 should pass
        desc_1000 = "x" * 1000
        result = service.validate_description(desc_1000)
        assert len(result) == 1000

        # 1001 should fail
        with pytest.raises(ValueError) as exc:
            service.validate_description("x" * 1001)
        assert "1000 characters" in str(exc.value)


class TestPriorityValidation:
    """Contract tests for priority validation (FR-P requirements)."""

    @pytest.fixture
    def service(self):
        """Create service for testing."""
        store = TaskStore()
        return TaskService(store)

    def test_priority_valid_values(self, service):
        """Priority accepts high, medium, low."""
        from src.models.task import Priority

        assert service.validate_priority("high") == Priority.HIGH
        assert service.validate_priority("medium") == Priority.MEDIUM
        assert service.validate_priority("low") == Priority.LOW

    def test_priority_case_insensitive(self, service):
        """Priority is case-insensitive."""
        from src.models.task import Priority

        assert service.validate_priority("HIGH") == Priority.HIGH
        assert service.validate_priority("MeDiUm") == Priority.MEDIUM

    def test_priority_invalid_error_message(self, service):
        """Invalid priority shows helpful error."""
        with pytest.raises(ValueError) as exc:
            service.validate_priority("urgent")
        assert "high, medium, low" in str(exc.value).lower()


class TestTagValidation:
    """Contract tests for tag validation (FR-T requirements)."""

    @pytest.fixture
    def service(self):
        """Create service for testing."""
        store = TaskStore()
        return TaskService(store)

    def test_tags_max_10(self, service):
        """Maximum 10 tags per task."""
        # 10 tags should pass
        tags_10 = ",".join([f"tag{i}" for i in range(10)])
        result = service.validate_tags(tags_10)
        assert len(result) == 10

        # 11 tags should fail
        tags_11 = ",".join([f"tag{i}" for i in range(11)])
        with pytest.raises(ValueError) as exc:
            service.validate_tags(tags_11)
        assert "10 tags" in str(exc.value)

    def test_tags_max_50_chars_each(self, service):
        """Each tag max 50 characters."""
        # 50 chars should pass
        tag_50 = "x" * 50
        result = service.validate_tags(tag_50)
        assert len(result[0]) == 50

        # 51 chars should fail
        tag_51 = "x" * 51
        with pytest.raises(ValueError) as exc:
            service.validate_tags(tag_51)
        assert "50 chars" in str(exc.value)

    def test_tags_alphanumeric_hyphen_underscore(self, service):
        """Tags allow alphanumeric, hyphens, underscores only."""
        # Valid characters
        result = service.validate_tags("work-related,home_tasks,tag123")
        assert result == ["work-related", "home_tasks", "tag123"]

        # Invalid characters
        with pytest.raises(ValueError) as exc:
            service.validate_tags("work@home")
        assert "Invalid tag format" in str(exc.value)

    def test_tags_lowercased(self, service):
        """Tags normalized to lowercase."""
        result = service.validate_tags("WORK,Home,uRgEnT")
        assert result == ["work", "home", "urgent"]

    def test_tags_deduplicated(self, service):
        """Duplicate tags removed."""
        result = service.validate_tags("work,work,home,home")
        assert result == ["work", "home"]


class TestDueDateValidation:
    """Contract tests for due date validation (FR-D requirements)."""

    @pytest.fixture
    def service(self):
        """Create service for testing."""
        store = TaskStore()
        return TaskService(store)

    def test_due_date_iso_format(self, service):
        """Due date accepts YYYY-MM-DD format."""
        future = date.today() + timedelta(days=7)
        result = service.validate_due_date(future.isoformat())
        assert result == future

    def test_due_date_invalid_format_error(self, service):
        """Invalid date format shows helpful error."""
        with pytest.raises(ValueError) as exc:
            service.validate_due_date("01-15-2025")
        assert "YYYY-MM-DD" in str(exc.value)

    def test_due_date_past_rejected(self, service):
        """Due date in the past rejected."""
        past = date.today() - timedelta(days=1)
        with pytest.raises(ValueError) as exc:
            service.validate_due_date(past.isoformat())
        assert "past" in str(exc.value).lower()

    def test_due_date_today_allowed(self, service):
        """Due date of today is allowed."""
        today = date.today()
        result = service.validate_due_date(today.isoformat())
        assert result == today

    def test_due_date_none_clears(self, service):
        """'none' clears due date."""
        result = service.validate_due_date("none")
        assert result is None


class TestDueTimeValidation:
    """Contract tests for due time validation."""

    @pytest.fixture
    def service(self):
        """Create service for testing."""
        store = TaskStore()
        return TaskService(store)

    def test_due_time_24h_format(self, service):
        """Due time accepts HH:MM 24-hour format."""
        from datetime import time as t

        result = service.validate_due_time("14:30", has_due_date=True)
        assert result == t(14, 30)

    def test_due_time_requires_due_date(self, service):
        """Due time requires due date to be set."""
        with pytest.raises(ValueError) as exc:
            service.validate_due_time("14:30", has_due_date=False)
        assert "requires a due date" in str(exc.value)

    def test_due_time_invalid_format_error(self, service):
        """Invalid time format shows helpful error."""
        with pytest.raises(ValueError) as exc:
            service.validate_due_time("2:30pm", has_due_date=True)
        assert "HH:MM" in str(exc.value)


class TestRecurrenceValidation:
    """Contract tests for recurrence validation (FR-R requirements)."""

    @pytest.fixture
    def service(self):
        """Create service for testing."""
        store = TaskStore()
        return TaskService(store)

    def test_recurrence_valid_values(self, service):
        """Recurrence accepts daily, weekly, monthly, none."""
        from src.models.task import Recurrence

        assert service.validate_recurrence("daily", True) == Recurrence.DAILY
        assert service.validate_recurrence("weekly", True) == Recurrence.WEEKLY
        assert service.validate_recurrence("monthly", True) == Recurrence.MONTHLY
        assert service.validate_recurrence("none", False) == Recurrence.NONE

    def test_recurrence_requires_due_date(self, service):
        """Recurring task requires due date."""
        with pytest.raises(ValueError) as exc:
            service.validate_recurrence("daily", has_due_date=False)
        assert "must have a due date" in str(exc.value)


class TestReminderThresholdValidation:
    """Contract tests for reminder threshold configuration."""

    def test_threshold_valid_formats(self):
        """Threshold accepts 1h, 6h, 12h, 24h, 48h, 7d."""
        from datetime import timedelta

        config = Config()

        config.set_threshold("1h")
        assert config.reminder_threshold == timedelta(hours=1)

        config.set_threshold("6h")
        assert config.reminder_threshold == timedelta(hours=6)

        config.set_threshold("12h")
        assert config.reminder_threshold == timedelta(hours=12)

        config.set_threshold("24h")
        assert config.reminder_threshold == timedelta(hours=24)

        config.set_threshold("48h")
        assert config.reminder_threshold == timedelta(hours=48)

        config.set_threshold("7d")
        assert config.reminder_threshold == timedelta(days=7)

    def test_threshold_invalid_format_error(self):
        """Invalid threshold format shows helpful error."""
        config = Config()

        with pytest.raises(ValueError) as exc:
            config.set_threshold("10m")  # Minutes not supported
        assert "1h, 6h, 12h, 24h, 48h, 7d" in str(exc.value)
