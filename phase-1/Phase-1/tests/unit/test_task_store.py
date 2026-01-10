"""Unit tests for TaskStore CRUD operations.

TDD: These tests are written FIRST and should FAIL until implementation is complete.
"""

import pytest
from datetime import datetime


class TestTaskStoreCRUD:
    """Tests for TaskStore CRUD operations (T015)."""

    @pytest.fixture
    def store(self):
        """Create fresh TaskStore for each test."""
        from src.services.task_store import TaskStore
        return TaskStore()

    def test_store_starts_empty(self, store):
        """New store should be empty."""
        assert store.list_all() == []
        assert store.count() == 0

    def test_add_task(self, store):
        """Store.add should create task with auto-generated ID."""
        from src.models.task import Task, Priority

        task = Task(id=0, title="Test Task")  # ID will be assigned by store
        created = store.add(task)

        assert created.id == 1
        assert created.title == "Test Task"
        assert store.count() == 1

    def test_add_multiple_tasks_increments_id(self, store):
        """Store should auto-increment IDs."""
        from src.models.task import Task

        task1 = store.add(Task(id=0, title="Task 1"))
        task2 = store.add(Task(id=0, title="Task 2"))
        task3 = store.add(Task(id=0, title="Task 3"))

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_get_task_by_id(self, store):
        """Store.get should return task by ID."""
        from src.models.task import Task

        created = store.add(Task(id=0, title="Test Task"))
        retrieved = store.get(created.id)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.title == "Test Task"

    def test_get_nonexistent_task_returns_none(self, store):
        """Store.get should return None for nonexistent ID."""
        result = store.get(999)
        assert result is None

    def test_update_task(self, store):
        """Store.update should modify task fields."""
        from src.models.task import Task, Priority

        created = store.add(Task(id=0, title="Original"))

        updated = store.update(
            created.id,
            title="Updated",
            description="New description",
            priority=Priority.HIGH
        )

        assert updated is not None
        assert updated.title == "Updated"
        assert updated.description == "New description"
        assert updated.priority == Priority.HIGH
        assert updated.updated_at > created.created_at

    def test_update_nonexistent_task_returns_none(self, store):
        """Store.update should return None for nonexistent ID."""
        result = store.update(999, title="Test")
        assert result is None

    def test_delete_task(self, store):
        """Store.delete should remove task."""
        from src.models.task import Task

        created = store.add(Task(id=0, title="To Delete"))

        assert store.delete(created.id) is True
        assert store.get(created.id) is None
        assert store.count() == 0

    def test_delete_nonexistent_task_returns_false(self, store):
        """Store.delete should return False for nonexistent ID."""
        result = store.delete(999)
        assert result is False

    def test_list_all_tasks(self, store):
        """Store.list_all should return all tasks."""
        from src.models.task import Task

        store.add(Task(id=0, title="Task 1"))
        store.add(Task(id=0, title="Task 2"))
        store.add(Task(id=0, title="Task 3"))

        all_tasks = store.list_all()

        assert len(all_tasks) == 3
        assert all_tasks[0].title == "Task 1"
        assert all_tasks[1].title == "Task 2"
        assert all_tasks[2].title == "Task 3"

    def test_count_tasks(self, store):
        """Store.count should return number of tasks."""
        from src.models.task import Task

        assert store.count() == 0

        store.add(Task(id=0, title="Task 1"))
        assert store.count() == 1

        store.add(Task(id=0, title="Task 2"))
        assert store.count() == 2

    def test_ids_not_reused_after_delete(self, store):
        """Store should not reuse IDs after deletion."""
        from src.models.task import Task

        task1 = store.add(Task(id=0, title="Task 1"))
        task2 = store.add(Task(id=0, title="Task 2"))

        store.delete(task1.id)

        task3 = store.add(Task(id=0, title="Task 3"))

        assert task3.id == 3  # Not 1 (reused)
