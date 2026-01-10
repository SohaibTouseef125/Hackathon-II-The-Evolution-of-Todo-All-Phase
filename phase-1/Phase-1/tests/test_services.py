"""
Unit tests for the TaskService.

This module contains unit tests for the TaskService class,
covering all business logic methods.
"""
import unittest
from todo_app.services import TaskService


class TestTaskService(unittest.TestCase):
    """Test cases for the TaskService."""

    def setUp(self):
        """Set up a fresh TaskService instance for each test."""
        self.service = TaskService()

    def test_add_task(self):
        """Test adding a task."""
        task = self.service.add_task("Test title", "Test description")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test title")
        self.assertEqual(task.description, "Test description")
        self.assertFalse(task.completed)

    def test_list_tasks(self):
        """Test listing tasks with different filters."""
        # Add some tasks
        self.service.add_task("Pending task 1")
        self.service.add_task("Pending task 2")
        completed_task = self.service.add_task("Completed task")
        self.service.mark_task_complete(completed_task.id)

        # All tasks
        all_tasks = self.service.list_tasks("all")
        self.assertEqual(len(all_tasks), 3)

        # Pending tasks
        pending_tasks = self.service.list_tasks("pending")
        self.assertEqual(len(pending_tasks), 2)
        for task in pending_tasks:
            self.assertFalse(task.completed)

        # Completed tasks
        completed_tasks = self.service.list_tasks("completed")
        self.assertEqual(len(completed_tasks), 1)
        for task in completed_tasks:
            self.assertTrue(task.completed)

    def test_update_task(self):
        """Test updating a task."""
        task = self.service.add_task("Original title", "Original description")

        result = self.service.update_task(task.id, "New title", "New description")
        self.assertTrue(result)

        updated_task = self.service.get_task(task.id)
        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(updated_task.description, "New description")

        # Test partial update
        result = self.service.update_task(task.id, title="Updated title")
        self.assertTrue(result)

        updated_task = self.service.get_task(task.id)
        self.assertEqual(updated_task.title, "Updated title")
        self.assertEqual(updated_task.description, "New description")

        # Test updating non-existent task
        result = self.service.update_task(999, "New title")
        self.assertFalse(result)

    def test_delete_task(self):
        """Test deleting a task."""
        task = self.service.add_task("Test title")
        task_id = task.id

        result = self.service.delete_task(task_id)
        self.assertTrue(result)
        self.assertIsNone(self.service.get_task(task_id))

        # Test deleting non-existent task
        result = self.service.delete_task(999)
        self.assertFalse(result)

    def test_mark_task_complete(self):
        """Test marking a task as complete."""
        task = self.service.add_task("Test title")

        result = self.service.mark_task_complete(task.id)
        self.assertTrue(result)

        updated_task = self.service.get_task(task.id)
        self.assertTrue(updated_task.completed)

        # Test marking non-existent task
        result = self.service.mark_task_complete(999)
        self.assertFalse(result)

    def test_mark_task_incomplete(self):
        """Test marking a task as incomplete."""
        task = self.service.add_task("Test title")
        self.service.mark_task_complete(task.id)  # First mark as complete

        result = self.service.mark_task_incomplete(task.id)
        self.assertTrue(result)

        updated_task = self.service.get_task(task.id)
        self.assertFalse(updated_task.completed)

        # Test marking non-existent task
        result = self.service.mark_task_incomplete(999)
        self.assertFalse(result)

    def test_get_task(self):
        """Test getting a specific task."""
        task = self.service.add_task("Test title")
        retrieved_task = self.service.get_task(task.id)

        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.id, task.id)
        self.assertEqual(retrieved_task.title, "Test title")

        # Test getting non-existent task
        retrieved_task = self.service.get_task(999)
        self.assertIsNone(retrieved_task)


if __name__ == '__main__':
    unittest.main()