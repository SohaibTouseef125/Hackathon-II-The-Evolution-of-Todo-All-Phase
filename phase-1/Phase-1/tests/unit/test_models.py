"""Unit tests for Task, Priority, Recurrence, and Config models.

TDD: These tests are written FIRST and should FAIL until implementation is complete.
"""

import pytest
from datetime import datetime, date, time, timedelta


class TestPriorityEnum:
    """Tests for Priority enum (T011)."""

    def test_priority_has_three_values(self):
        """Priority enum should have exactly HIGH, MEDIUM, LOW values."""
        from src.models.task import Priority

        assert Priority.HIGH.value == "high"
        assert Priority.MEDIUM.value == "medium"
        assert Priority.LOW.value == "low"
        assert len(Priority) == 3

    def test_priority_from_string_case_insensitive(self):
        """Priority.from_string should parse case-insensitively."""
        from src.models.task import Priority

        assert Priority.from_string("high") == Priority.HIGH
        assert Priority.from_string("HIGH") == Priority.HIGH
        assert Priority.from_string("High") == Priority.HIGH
        assert Priority.from_string("medium") == Priority.MEDIUM
        assert Priority.from_string("low") == Priority.LOW

    def test_priority_from_string_invalid(self):
        """Priority.from_string should raise ValueError for invalid input."""
        from src.models.task import Priority

        with pytest.raises(ValueError):
            Priority.from_string("invalid")
        with pytest.raises(ValueError):
            Priority.from_string("")

    def test_priority_sort_key(self):
        """Priority.sort_key should return correct ordering values."""
        from src.models.task import Priority

        assert Priority.HIGH.sort_key() == 1
        assert Priority.MEDIUM.sort_key() == 2
        assert Priority.LOW.sort_key() == 3

    def test_priority_sort_order(self):
        """Priorities should sort correctly: HIGH < MEDIUM < LOW."""
        from src.models.task import Priority

        priorities = [Priority.LOW, Priority.HIGH, Priority.MEDIUM]
        sorted_priorities = sorted(priorities, key=lambda p: p.sort_key())

        assert sorted_priorities == [Priority.HIGH, Priority.MEDIUM, Priority.LOW]


class TestRecurrenceEnum:
    """Tests for Recurrence enum (T012)."""

    def test_recurrence_has_four_values(self):
        """Recurrence enum should have DAILY, WEEKLY, MONTHLY, NONE values."""
        from src.models.task import Recurrence

        assert Recurrence.DAILY.value == "daily"
        assert Recurrence.WEEKLY.value == "weekly"
        assert Recurrence.MONTHLY.value == "monthly"
        assert Recurrence.NONE.value == "none"
        assert len(Recurrence) == 4

    def test_recurrence_from_string_case_insensitive(self):
        """Recurrence.from_string should parse case-insensitively."""
        from src.models.task import Recurrence

        assert Recurrence.from_string("daily") == Recurrence.DAILY
        assert Recurrence.from_string("WEEKLY") == Recurrence.WEEKLY
        assert Recurrence.from_string("Monthly") == Recurrence.MONTHLY
        assert Recurrence.from_string("none") == Recurrence.NONE

    def test_recurrence_from_string_invalid(self):
        """Recurrence.from_string should raise ValueError for invalid input."""
        from src.models.task import Recurrence

        with pytest.raises(ValueError):
            Recurrence.from_string("yearly")
        with pytest.raises(ValueError):
            Recurrence.from_string("")


class TestTaskDataclass:
    """Tests for Task dataclass basic fields (T013)."""

    def test_task_creation_with_required_fields(self):
        """Task should be created with required fields."""
        from src.models.task import Task, Priority, Recurrence

        task = Task(id=1, title="Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description is None
        assert task.completed is False
        assert task.priority == Priority.MEDIUM
        assert task.tags == []
        assert task.due_date is None
        assert task.due_time is None
        assert task.recurrence == Recurrence.NONE

    def test_task_creation_with_all_fields(self):
        """Task should be created with all fields specified."""
        from src.models.task import Task, Priority, Recurrence

        due = date(2025, 1, 15)
        due_t = time(14, 30)

        task = Task(
            id=1,
            title="Full Task",
            description="A complete task",
            completed=True,
            priority=Priority.HIGH,
            tags=["work", "urgent"],
            due_date=due,
            due_time=due_t,
            recurrence=Recurrence.DAILY
        )

        assert task.id == 1
        assert task.title == "Full Task"
        assert task.description == "A complete task"
        assert task.completed is True
        assert task.priority == Priority.HIGH
        assert task.tags == ["work", "urgent"]
        assert task.due_date == due
        assert task.due_time == due_t
        assert task.recurrence == Recurrence.DAILY

    def test_task_has_timestamps(self):
        """Task should have created_at and updated_at timestamps."""
        from src.models.task import Task

        before = datetime.now()
        task = Task(id=1, title="Test")
        after = datetime.now()

        assert task.created_at is not None
        assert task.updated_at is not None
        assert before <= task.created_at <= after
        assert before <= task.updated_at <= after

    def test_task_tags_default_empty_list(self):
        """Task tags should default to empty list, not shared mutable."""
        from src.models.task import Task

        task1 = Task(id=1, title="Task 1")
        task2 = Task(id=2, title="Task 2")

        task1.tags.append("test")

        assert task1.tags == ["test"]
        assert task2.tags == []  # Should not be affected


class TestConfigDataclass:
    """Tests for Config dataclass (T014)."""

    def test_config_default_threshold(self):
        """Config should default to 24 hour reminder threshold."""
        from src.models.config import Config

        config = Config()

        assert config.reminder_threshold == timedelta(hours=24)

    def test_config_set_threshold_hours(self):
        """Config.set_threshold should parse hour format."""
        from src.models.config import Config

        config = Config()

        config.set_threshold("1h")
        assert config.reminder_threshold == timedelta(hours=1)

        config.set_threshold("12h")
        assert config.reminder_threshold == timedelta(hours=12)

        config.set_threshold("48h")
        assert config.reminder_threshold == timedelta(hours=48)

    def test_config_set_threshold_days(self):
        """Config.set_threshold should parse day format."""
        from src.models.config import Config

        config = Config()

        config.set_threshold("7d")
        assert config.reminder_threshold == timedelta(days=7)

    def test_config_set_threshold_invalid(self):
        """Config.set_threshold should raise ValueError for invalid format."""
        from src.models.config import Config

        config = Config()

        with pytest.raises(ValueError):
            config.set_threshold("invalid")
        with pytest.raises(ValueError):
            config.set_threshold("10m")  # Minutes not supported
        with pytest.raises(ValueError):
            config.set_threshold("")

    def test_config_get_threshold_display(self):
        """Config.get_threshold_display should return human-readable string."""
        from src.models.config import Config

        config = Config()

        config.set_threshold("24h")
        assert config.get_threshold_display() == "24h"

        config.set_threshold("7d")
        assert config.get_threshold_display() == "7d"
