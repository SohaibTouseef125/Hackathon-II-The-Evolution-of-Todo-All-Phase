"""
Command-line interface for the todo application.

This module contains the CLI handlers that process user commands
and interact with the TaskService to perform operations.

The CLI implements all the command patterns specified in the contracts,
providing a user-friendly interface for all todo operations with proper
error handling and formatted output.
"""
import argparse
from typing import Optional
from .services import TaskService
import colorama
from colorama import Fore, Back, Style


class TodoCLI:
    """
    Command-line interface for the todo application.
    """
    def __init__(self):
        """Initialize the CLI with a TaskService instance and initialize colorama."""
        colorama.init()
        self.service = TaskService()

    def add_task(self, title: str, description: str = "") -> str:
        """
        Add a new task with title and optional description.

        Args:
            title: Title of the task
            description: Optional description of the task

        Returns:
            Confirmation message with task ID
        """
        try:
            task = self.service.add_task(title, description or "")
            message = f"✓ Task added successfully with ID: {task.id}"
            return f"{Fore.GREEN}{message}{Style.RESET_ALL}" if self._is_interactive_mode() else message
        except ValueError as e:
            error_msg = f"✗ Error adding task: {str(e)}"
            return f"{Fore.RED}{error_msg}{Style.RESET_ALL}" if self._is_interactive_mode() else error_msg

    def _is_interactive_mode(self) -> bool:
        """
        Check if we're in interactive mode to determine if colors should be applied.
        For testing purposes, we return False to avoid ANSI codes in test output.
        """
        import os
        # Check if we're running in a test environment or if stdout is being redirected
        return os.isatty(0) and os.isatty(1) and 'PYTEST_CURRENT_TEST' not in os.environ

    def list_tasks(self, status: str = "all") -> str:
        """
        List all tasks or filtered by status.

        Args:
            status: Filter by status ('all', 'pending', 'completed')

        Returns:
            Formatted list of tasks
        """
        tasks = self.service.list_tasks(status)
        if not tasks:
            message = "No tasks found."
            return f"{Fore.YELLOW}{message}{Style.RESET_ALL}" if self._is_interactive_mode() else message

        output_lines = []

        # Create the header and separator
        header = f"{'ID':<4} {'Status':<10} {'Title':<30} {'Description'}"
        separator = f"{'-' * 70}"

        if self._is_interactive_mode():
            header = f"{Fore.CYAN}{header}{Style.RESET_ALL}"
            separator = f"{Fore.CYAN}{separator}{Style.RESET_ALL}"

        output_lines.append(header)
        output_lines.append(separator)

        for task in tasks:
            if self._is_interactive_mode():
                if task.completed:
                    status_str = f"{Fore.GREEN}✓{Style.RESET_ALL}"
                    title_color = f"{Fore.GREEN}{task.title[:27] + '...' if len(task.title) > 30 else task.title}{Style.RESET_ALL}"
                else:
                    status_str = f"{Fore.YELLOW}○{Style.RESET_ALL}"
                    title_color = f"{Fore.WHITE}{task.title[:27] + '...' if len(task.title) > 30 else task.title}{Style.RESET_ALL}"

                id_str = f"{Fore.BLUE}{task.id:<4}{Style.RESET_ALL}"
                desc = task.description[:30] + "..." if len(task.description) > 30 else task.description
                output_lines.append(f"{id_str} {status_str:<10} {title_color:<30} {desc}")
            else:
                # Plain text for testing
                status_str = "✓" if task.completed else "○"
                title = task.title[:27] + "..." if len(task.title) > 30 else task.title
                desc = task.description[:30] + "..." if len(task.description) > 30 else task.description
                output_lines.append(f"{task.id:<4} {status_str:<10} {title:<30} {desc}")

        return "\n".join(output_lines)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> str:
        """
        Update an existing task.

        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            Confirmation message
        """
        try:
            success = self.service.update_task(task_id, title, description)
            if success:
                message = f"✓ Task {task_id} updated successfully."
                return f"{Fore.GREEN}{message}{Style.RESET_ALL}" if self._is_interactive_mode() else message
            else:
                message = f"✗ Task with ID {task_id} not found."
                return f"{Fore.RED}{message}{Style.RESET_ALL}" if self._is_interactive_mode() else message
        except ValueError as e:
            error_msg = f"✗ Error updating task: {str(e)}"
            return f"{Fore.RED}{error_msg}{Style.RESET_ALL}" if self._is_interactive_mode() else error_msg

    def delete_task(self, task_id: int) -> str:
        """
        Delete a task by its ID.

        Args:
            task_id: ID of the task to delete

        Returns:
            Confirmation message
        """
        success = self.service.delete_task(task_id)
        if success:
            message = f"✓ Task {task_id} deleted successfully."
            return f"{Fore.GREEN}{message}{Style.RESET_ALL}" if self._is_interactive_mode() else message
        else:
            message = f"✗ Task with ID {task_id} not found."
            return f"{Fore.RED}{message}{Style.RESET_ALL}" if self._is_interactive_mode() else message

    def complete_task(self, task_id: int) -> str:
        """
        Mark a task as complete.

        Args:
            task_id: ID of the task to mark complete

        Returns:
            Confirmation message
        """
        success = self.service.mark_task_complete(task_id)
        if success:
            message = f"✓ Task {task_id} marked as complete."
            return f"{Fore.GREEN}{message}{Style.RESET_ALL}" if self._is_interactive_mode() else message
        else:
            message = f"✗ Task with ID {task_id} not found."
            return f"{Fore.RED}{message}{Style.RESET_ALL}" if self._is_interactive_mode() else message

    def incomplete_task(self, task_id: int) -> str:
        """
        Mark a task as incomplete.

        Args:
            task_id: ID of the task to mark incomplete

        Returns:
            Confirmation message
        """
        success = self.service.mark_task_incomplete(task_id)
        if success:
            message = f"✓ Task {task_id} marked as incomplete."
            return f"{Fore.GREEN}{message}{Style.RESET_ALL}" if self._is_interactive_mode() else message
        else:
            message = f"✗ Task with ID {task_id} not found."
            return f"{Fore.RED}{message}{Style.RESET_ALL}" if self._is_interactive_mode() else message

    def interactive_menu(self):
        """Run the interactive menu interface with colors."""
        while True:
            self._clear_screen()
            print(f"\n{Back.BLUE}{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
            print(f"{Back.BLUE}{Fore.WHITE}{'TODO APPLICATION - MAIN MENU':^60}{Style.RESET_ALL}")
            print(f"{Back.BLUE}{Fore.WHITE}{'='*60}{Style.RESET_ALL}")

            print(f"\n{Fore.CYAN}1. 📝 Add Task{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}2. 📋 List Tasks{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}3. ✏️  Update Task{Style.RESET_ALL}")
            print(f"{Fore.RED}4. 🗑️  Delete Task{Style.RESET_ALL}")
            print(f"{Fore.GREEN}5. ✅ Mark Task Complete{Style.RESET_ALL}")
            print(f"{Fore.BLUE}6. 🔄 Mark Task Incomplete{Style.RESET_ALL}")
            print(f"{Fore.WHITE}7. 🚪 Exit{Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}{'-'*60}{Style.RESET_ALL}")

            try:
                choice = input(f"{Fore.YELLOW}Select an option (1-7): {Style.RESET_ALL}").strip()

                if choice == "1":
                    self._interactive_add_task()
                elif choice == "2":
                    self._interactive_list_tasks()
                elif choice == "3":
                    self._interactive_update_task()
                elif choice == "4":
                    self._interactive_delete_task()
                elif choice == "5":
                    self._interactive_complete_task()
                elif choice == "6":
                    self._interactive_incomplete_task()
                elif choice == "7":
                    print(f"\n{Fore.CYAN}Thank you for using the Todo Application!{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED}✗ Invalid option. Please select 1-7.{Style.RESET_ALL}")

                input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n\n{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}✗ An error occurred: {str(e)}{Style.RESET_ALL}")
                input(f"{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")

    def _clear_screen(self):
        """Clear the terminal screen."""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    def _interactive_add_task(self):
        """Interactive task addition with colors."""
        print(f"\n{Back.CYAN}{Fore.BLACK}--- Add New Task ---{Style.RESET_ALL}")
        title = input(f"{Fore.CYAN}Enter task title: {Style.RESET_ALL}").strip()
        if not title:
            print(f"{Fore.RED}✗ Title cannot be empty.{Style.RESET_ALL}")
            return

        description = input(f"{Fore.CYAN}Enter task description (optional, press Enter to skip): {Style.RESET_ALL}").strip()

        result = self.add_task(title, description)
        print(result)

    def _interactive_list_tasks(self):
        """Interactive task listing with colors."""
        print(f"\n{Back.YELLOW}{Fore.BLACK}--- List Tasks ---{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Filter options:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. All tasks{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2. Pending tasks only{Style.RESET_ALL}")
        print(f"{Fore.RED}3. Completed tasks only{Style.RESET_ALL}")

        filter_choice = input(f"{Fore.CYAN}Select filter (1-3, default 1): {Style.RESET_ALL}").strip()
        status_map = {"1": "all", "2": "pending", "3": "completed"}
        status = status_map.get(filter_choice, "all")

        result = self.list_tasks(status)
        print(result)

    def _interactive_update_task(self):
        """Interactive task update with colors."""
        print(f"\n{Back.MAGENTA}{Fore.BLACK}--- Update Task ---{Style.RESET_ALL}")
        try:
            task_id = int(input(f"{Fore.MAGENTA}Enter task ID to update: {Style.RESET_ALL}"))
        except ValueError:
            print(f"{Fore.RED}✗ Invalid task ID. Please enter a number.{Style.RESET_ALL}")
            return

        print(f"{Fore.CYAN}Leave blank to keep current value{Style.RESET_ALL}")
        new_title = input(f"{Fore.CYAN}Enter new title (or press Enter to keep current): {Style.RESET_ALL}").strip()
        new_desc = input(f"{Fore.CYAN}Enter new description (or press Enter to keep current): {Style.RESET_ALL}").strip()

        # Convert empty strings to None to keep current values
        title = new_title if new_title else None
        description = new_desc if new_desc else None

        result = self.update_task(task_id, title, description)
        print(result)

    def _interactive_delete_task(self):
        """Interactive task deletion with colors."""
        print(f"\n{Back.RED}{Fore.WHITE}--- Delete Task ---{Style.RESET_ALL}")
        try:
            task_id = int(input(f"{Fore.RED}Enter task ID to delete: {Style.RESET_ALL}"))
            result = self.delete_task(task_id)
            print(result)
        except ValueError:
            print(f"{Fore.RED}✗ Invalid task ID. Please enter a number.{Style.RESET_ALL}")

    def _interactive_complete_task(self):
        """Interactive task completion with colors."""
        print(f"\n{Back.GREEN}{Fore.WHITE}--- Mark Task Complete ---{Style.RESET_ALL}")
        try:
            task_id = int(input(f"{Fore.GREEN}Enter task ID to mark complete: {Style.RESET_ALL}"))
            result = self.complete_task(task_id)
            print(result)
        except ValueError:
            print(f"{Fore.RED}✗ Invalid task ID. Please enter a number.{Style.RESET_ALL}")

    def _interactive_incomplete_task(self):
        """Interactive task incompleteness with colors."""
        print(f"\n{Back.BLUE}{Fore.WHITE}--- Mark Task Incomplete ---{Style.RESET_ALL}")
        try:
            task_id = int(input(f"{Fore.BLUE}Enter task ID to mark incomplete: {Style.RESET_ALL}"))
            result = self.incomplete_task(task_id)
            print(result)
        except ValueError:
            print(f"{Fore.RED}✗ Invalid task ID. Please enter a number.{Style.RESET_ALL}")

    def run(self, args: Optional[argparse.Namespace] = None) -> None:
        """
        Run the CLI with parsed arguments.

        Args:
            args: Parsed command line arguments (if None, parse from sys.argv)
        """
        if args is None:
            # Check if any command-line arguments were provided
            import sys
            if len(sys.argv) > 1:
                # Use command-line parsing for direct commands
                parser = self.create_parser()
                args = parser.parse_args()

                # Execute the command based on the arguments
                if args.command == "add":
                    result = self.add_task(args.title, getattr(args, 'description', ''))
                    print(result)
                elif args.command == "list":
                    result = self.list_tasks(args.status)
                    print(result)
                elif args.command == "update":
                    result = self.update_task(args.id, args.title, args.description)
                    print(result)
                elif args.command == "delete":
                    result = self.delete_task(args.id)
                    print(result)
                elif args.command == "complete":
                    result = self.complete_task(args.id)
                    print(result)
                elif args.command == "incomplete":
                    result = self.incomplete_task(args.id)
                    print(result)
                else:
                    # If no command provided, show interactive menu
                    self.interactive_menu()
            else:
                # No arguments provided, show interactive menu
                self.interactive_menu()
        else:
            # Execute the command based on the arguments
            if args.command == "add":
                result = self.add_task(args.title, getattr(args, 'description', ''))
                print(result)
            elif args.command == "list":
                result = self.list_tasks(args.status)
                print(result)
            elif args.command == "update":
                result = self.update_task(args.id, args.title, args.description)
                print(result)
            elif args.command == "delete":
                result = self.delete_task(args.id)
                print(result)
            elif args.command == "complete":
                result = self.complete_task(args.id)
                print(result)
            elif args.command == "incomplete":
                result = self.incomplete_task(args.id)
                print(result)
            else:
                self.interactive_menu()

    def create_parser(self) -> argparse.ArgumentParser:
        """
        Create the argument parser with all available commands.

        Returns:
            Configured ArgumentParser
        """
        parser = argparse.ArgumentParser(
            prog="todo-app",
            description="Todo application command-line interface"
        )
        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Add command
        add_parser = subparsers.add_parser("add", help="Add a new task")
        add_parser.add_argument("title", help="Title of the task")
        add_parser.add_argument("--description", "-d", help="Description of the task")

        # List command
        list_parser = subparsers.add_parser("list", help="List all tasks")
        list_parser.add_argument(
            "--status",
            choices=["all", "pending", "completed"],
            default="all",
            help="Filter tasks by status (default: all)"
        )

        # Update command
        update_parser = subparsers.add_parser("update", help="Update an existing task")
        update_parser.add_argument("id", type=int, help="ID of the task to update")
        update_parser.add_argument("--title", help="New title for the task")
        update_parser.add_argument("--description", "-d", help="New description for the task")

        # Delete command
        delete_parser = subparsers.add_parser("delete", help="Delete a task")
        delete_parser.add_argument("id", type=int, help="ID of the task to delete")

        # Complete command
        complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
        complete_parser.add_argument("id", type=int, help="ID of the task to mark complete")

        # Incomplete command
        incomplete_parser = subparsers.add_parser("incomplete", help="Mark a task as incomplete")
        incomplete_parser.add_argument("id", type=int, help="ID of the task to mark incomplete")

        return parser