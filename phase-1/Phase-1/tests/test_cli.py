"""
Integration tests for the CLI interface.

This module contains integration tests for the TodoCLI class,
testing the command-line interface functionality.
"""
import unittest
import sys
from io import StringIO
from unittest.mock import patch
from todo_app.cli import TodoCLI


class TestTodoCLI(unittest.TestCase):
    """Test cases for the CLI interface."""

    def setUp(self):
        """Set up a fresh CLI instance for each test."""
        self.cli = TodoCLI()

    def test_add_task(self):
        """Test adding a task via CLI."""
        result = self.cli.add_task("Test task", "Test description")
        self.assertIn("Task added successfully", result)
        self.assertIn("ID:", result)

        # Test without description
        result = self.cli.add_task("Test task 2")
        self.assertIn("Task added successfully", result)

    def test_list_tasks(self):
        """Test listing tasks via CLI."""
        # Add some tasks first
        self.cli.add_task("Pending task")
        completed_task_result = self.cli.add_task("Completed task")
        # Extract ID from the result: "Task added successfully with ID: X"
        task_id = int(completed_task_result.split()[-1])  # Get the ID
        self.cli.complete_task(task_id)  # Mark the task as complete using the ID

        # List all tasks
        result = self.cli.list_tasks("all")
        self.assertIn("Pending task", result)
        self.assertIn("Completed task", result)
        self.assertNotIn("No tasks found", result)  # Ensure tasks are found

        # List pending tasks
        result = self.cli.list_tasks("pending")
        self.assertIn("Pending task", result)
        self.assertNotIn("Completed task", result)

        # List completed tasks
        result = self.cli.list_tasks("completed")
        self.assertIn("Completed task", result)
        self.assertNotIn("Pending task", result)

    def test_update_task(self):
        """Test updating a task via CLI."""
        # Add a task first
        add_result = self.cli.add_task("Original title", "Original description")
        task_id = int(add_result.split()[-1])  # Extract ID from "Task added successfully with ID: X"

        # Update the task
        result = self.cli.update_task(task_id, "New title", "New description")
        self.assertIn("updated successfully", result)

        # Verify the update by listing tasks
        list_result = self.cli.list_tasks("all")
        self.assertIn("New title", list_result)

    def test_delete_task(self):
        """Test deleting a task via CLI."""
        # Add a task first
        add_result = self.cli.add_task("Task to delete")
        task_id = int(add_result.split()[-1])  # Extract ID

        # Delete the task
        result = self.cli.delete_task(task_id)
        self.assertIn("deleted successfully", result)

        # Verify the task is gone
        list_result = self.cli.list_tasks("all")
        self.assertNotIn("Task to delete", list_result)

    def test_complete_task(self):
        """Test marking a task as complete via CLI."""
        # Add a task first
        add_result = self.cli.add_task("Task to complete")
        task_id = int(add_result.split()[-1])  # Extract ID

        # Mark as complete
        result = self.cli.complete_task(task_id)
        self.assertIn("marked as complete", result)

        # Verify it's marked as complete
        list_result = self.cli.list_tasks("completed")
        self.assertIn("Task to complete", list_result)

    def test_incomplete_task(self):
        """Test marking a task as incomplete via CLI."""
        # Add and complete a task first
        add_result = self.cli.add_task("Task to mark incomplete")
        task_id = int(add_result.split()[-1])  # Extract ID
        self.cli.complete_task(task_id)

        # Mark as incomplete
        result = self.cli.incomplete_task(task_id)
        self.assertIn("marked as incomplete", result)

        # Verify it's marked as incomplete
        list_result = self.cli.list_tasks("pending")
        self.assertIn("Task to mark incomplete", list_result)

    def test_error_handling_invalid_task_id(self):
        """Test error handling for invalid task IDs."""
        result = self.cli.update_task(999, "New title")
        self.assertIn("not found", result)

        result = self.cli.delete_task(999)
        self.assertIn("not found", result)

        result = self.cli.complete_task(999)
        self.assertIn("not found", result)

        result = self.cli.incomplete_task(999)
        self.assertIn("not found", result)

    @patch('sys.argv', ['todo-app', 'add', 'Test task from argv'])
    def test_run_with_add_command(self):
        """Test running CLI with add command via argv."""
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            self.cli.run()
            output = captured_output.getvalue().strip()
            self.assertIn("Task added successfully", output)
        finally:
            # Restore stdout
            sys.stdout = sys.__stdout__

    @patch('sys.argv', ['todo-app', 'list'])
    def test_run_with_list_command(self):
        """Test running CLI with list command via argv."""
        # Add a task first
        self.cli.add_task("Test task for listing")

        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            self.cli.run()
            output = captured_output.getvalue().strip()
            self.assertIn("Test task for listing", output)
        finally:
            # Restore stdout
            sys.stdout = sys.__stdout__


if __name__ == '__main__':
    unittest.main()