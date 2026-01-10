"""
Unit tests for the Task and TaskList models.

This module contains unit tests for the Task and TaskList classes,
covering functionality and edge cases.
"""
import unittest
from datetime import datetime
from todo_app.models import Task, TaskList


class TestTask(unittest.TestCase):
    """Test cases for the Task model."""

    def test_create_task_valid(self):
        """Test creating a task with valid parameters."""
        task = Task(1, "Test title", "Test description")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test title")
        self.assertEqual(task.description, "Test description")
        self.assertFalse(task.completed)
        self.assertIsInstance(task.created_at, datetime)

    def test_create_task_defaults(self):
        """Test creating a task with default values."""
        task = Task(1, "Test title")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test title")
        self.assertEqual(task.description, "")
        self.assertFalse(task.completed)

    def test_task_title_validation(self):
        """Test title validation rules."""
        # Title too short
        with self.assertRaises(ValueError):
            Task(1, "")

        # Title too long
        with self.assertRaises(ValueError):
            Task(1, "a" * 201)  # 201 characters

        # Valid title
        task = Task(1, "Valid title")
        self.assertEqual(task.title, "Valid title")

    def test_task_description_validation(self):
        """Test description validation rules."""
        # Description too long
        with self.assertRaises(ValueError):
            Task(1, "Valid title", "a" * 1001)  # 1001 characters

        # Valid description
        task = Task(1, "Valid title", "a" * 1000)  # 1000 characters
        self.assertEqual(len(task.description), 1000)

    def test_update_task(self):
        """Test updating task properties."""
        task = Task(1, "Original title", "Original description")

        task.update("New title", "New description")
        self.assertEqual(task.title, "New title")
        self.assertEqual(task.description, "New description")

        # Test partial update
        task.update(title="Updated title")
        self.assertEqual(task.title, "Updated title")
        self.assertEqual(task.description, "New description")

    def test_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(1, "Test title", "Test description")
        task.completed = True

        task_dict = task.to_dict()
        self.assertEqual(task_dict['id'], 1)
        self.assertEqual(task_dict['title'], "Test title")
        self.assertEqual(task_dict['description'], "Test description")
        self.assertTrue(task_dict['completed'])
        self.assertIn('created_at', task_dict)


class TestTaskList(unittest.TestCase):
    """Test cases for the TaskList model."""

    def test_add_task(self):
        """Test adding a task to the list."""
        task_list = TaskList()
        task = task_list.add_task("Test title", "Test description")

        self.assertEqual(len(task_list.tasks), 1)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test title")
        self.assertEqual(task.description, "Test description")

    def test_get_task_by_id(self):
        """Test retrieving a task by ID."""
        task_list = TaskList()
        task = task_list.add_task("Test title")

        retrieved_task = task_list.get_task_by_id(1)
        self.assertEqual(retrieved_task.id, 1)
        self.assertEqual(retrieved_task.title, "Test title")

        # Test non-existent task
        non_existent = task_list.get_task_by_id(999)
        self.assertIsNone(non_existent)

    def test_update_task(self):
        """Test updating a task."""
        task_list = TaskList()
        task = task_list.add_task("Original title")

        result = task_list.update_task(1, "New title", "New description")
        self.assertTrue(result)

        updated_task = task_list.get_task_by_id(1)
        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(updated_task.description, "New description")

        # Test updating non-existent task
        result = task_list.update_task(999, "New title")
        self.assertFalse(result)

    def test_delete_task(self):
        """Test deleting a task."""
        task_list = TaskList()
        task_list.add_task("Test title")

        result = task_list.delete_task(1)
        self.assertTrue(result)
        self.assertEqual(len(task_list.tasks), 0)

        # Test deleting non-existent task
        result = task_list.delete_task(999)
        self.assertFalse(result)

    def test_list_tasks(self):
        """Test listing tasks with different filters."""
        task_list = TaskList()
        task_list.add_task("Task 1")
        task_list.add_task("Task 2")
        task_list.mark_task_complete(2)  # Mark second task as complete

        # All tasks
        all_tasks = task_list.list_tasks("all")
        self.assertEqual(len(all_tasks), 2)

        # Pending tasks
        pending_tasks = task_list.list_tasks("pending")
        self.assertEqual(len(pending_tasks), 1)
        self.assertFalse(pending_tasks[0].completed)

        # Completed tasks
        completed_tasks = task_list.list_tasks("completed")
        self.assertEqual(len(completed_tasks), 1)
        self.assertTrue(completed_tasks[0].completed)

    def test_toggle_completion(self):
        """Test toggling task completion status."""
        task_list = TaskList()
        task_list.add_task("Test title")

        # Initially pending
        task = task_list.get_task_by_id(1)
        self.assertFalse(task.completed)

        # Toggle to complete
        result = task_list.toggle_completion(1)
        self.assertTrue(result)
        task = task_list.get_task_by_id(1)
        self.assertTrue(task.completed)

        # Toggle back to pending
        result = task_list.toggle_completion(1)
        self.assertTrue(result)
        task = task_list.get_task_by_id(1)
        self.assertFalse(task.completed)

        # Toggle non-existent task
        result = task_list.toggle_completion(999)
        self.assertFalse(result)

    def test_mark_task_complete_incomplete(self):
        """Test marking tasks as complete/incomplete."""
        task_list = TaskList()
        task_list.add_task("Test title")

        # Mark complete
        result = task_list.mark_task_complete(1)
        self.assertTrue(result)
        task = task_list.get_task_by_id(1)
        self.assertTrue(task.completed)

        # Mark incomplete
        result = task_list.mark_task_incomplete(1)
        self.assertTrue(result)
        task = task_list.get_task_by_id(1)
        self.assertFalse(task.completed)

    def test_task_limit(self):
        """Test the maximum task limit."""
        task_list = TaskList()

        # Add 100 tasks (the limit)
        for i in range(100):
            task_list.add_task(f"Task {i}")

        # Try to add one more
        with self.assertRaises(ValueError):
            task_list.add_task("This should fail")

    def test_unique_ids(self):
        """Test that IDs are unique."""
        task_list = TaskList()
        task1 = task_list.add_task("Task 1")
        task2 = task_list.add_task("Task 2")

        self.assertEqual(task1.id, 1)
        self.assertEqual(task2.id, 2)
        self.assertNotEqual(task1.id, task2.id)


if __name__ == '__main__':
    unittest.main()