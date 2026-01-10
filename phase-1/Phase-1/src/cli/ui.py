"""Interactive terminal UI for Todo Extended application.

This module provides a colorful, menu-driven interface with keyboard navigation
for managing tasks using the rich library.
"""

from datetime import date, time as dt_time
from typing import Optional, List, Tuple
from enum import Enum

from rich.console import Console
from rich.theme import Theme
from rich.style import Style
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.align import Align
from rich.box import DOUBLE, ROUNDED
from rich.color import Color
from rich import box

from src.models.task import Task, Priority, Recurrence
from src.models.config import get_config
from src.services.task_store import get_store
from src.services.task_service import TaskService
from src.cli.formatters import format_task, format_task_created, format_task_updated


# Custom theme with colorful styles
custom_theme = Theme({
    "header": "bold cyan",
    "title": "bold magenta",
    "menu": "bold green",
    "menu_selected": "bold white on green",
    "task_high": "bold red",
    "task_medium": "bold yellow",
    "task_low": "bold blue",
    "task_completed": "dim green",
    "tag": "italic cyan",
    "due": "italic orange3",
    "recurring": "italic purple",
    "info": "dim white",
    "error": "bold red",
    "success": "bold green",
    "prompt": "bold yellow",
    "divider": "cyan",
})

console = Console(theme=custom_theme)


class MenuOption(Enum):
    """Menu navigation options."""
    UP = "up"
    DOWN = "down"
    SELECT = "select"
    BACK = "back"
    QUIT = "quit"
    ADD = "add"
    EDIT = "edit"
    DELETE = "delete"
    COMPLETE = "complete"
    SEARCH = "search"
    FILTER = "filter"
    HELP = "help"


class TodoUI:
    """Interactive terminal UI for Todo Extended."""

    def __init__(self):
        """Initialize the UI with console and services."""
        self.console = console
        self.store = get_store()
        self.service = TaskService(self.store)
        self.config = get_config()
        self.running = True
        self.current_menu = "main"

    def clear_screen(self):
        """Clear the terminal screen."""
        console.clear()

    def print_header(self, title: str):
        """Print a styled header."""
        header = Panel(
            Text(title, style="header", justify="center"),
            box=DOUBLE,
            style="cyan",
            subtitle="Use ↑/↓ to navigate, Enter to select, ESC for menu, 'q' to quit",
            subtitle_align="center",
        )
        console.print(header)

    def print_menu_item(self, text: str, index: int, selected: bool, shortcut: Optional[str] = None):
        """Print a menu item with styling based on selection state."""
        if selected:
            style = Style(color="white", bgcolor="green", bold=True)
            prefix = "▶ "
        else:
            style = Style(color="white", bold=True)
            prefix = "  "

        if shortcut:
            line = f"{prefix}[{shortcut}] {text}"
        else:
            line = f"{prefix}{text}"

        console.print(Text(line, style=style))

    def print_divider(self):
        """Print a decorative divider."""
        console.print("─" * 50, style="divider")

    def print_success(self, message: str):
        """Print a success message."""
        console.print(f"[success]✓ {message}[/success]")

    def print_error(self, message: str):
        """Print an error message."""
        console.print(f"[error]✗ {message}[/error]")

    def print_info(self, message: str):
        """Print an info message."""
        console.print(f"[info]ℹ {message}[/info]")

    def show_main_menu(self) -> str:
        """Display the main menu and return selected option."""
        self.clear_screen()

        # Show welcome panel
        welcome = Panel(
            Text(
                "TODO EXTENDED\nYour Colorful Task Manager",
                style="title bold",
                justify="center",
            ),
            box=ROUNDED,
            style="magenta",
            subtitle="Manage tasks with priorities, tags, due dates, and reminders",
            subtitle_align="center",
        )
        console.print(welcome)
        console.print()

        # Task statistics
        stats = self._get_task_stats()
        stats_panel = Panel(
            f"Total Tasks: {stats['total']}  |  "
            f"Pending: {stats['pending']}  |  "
            f"Completed: {stats['completed']}\n"
            f"High Priority: {stats['high']}  |  "
            f"Overdue: {stats['overdue']}  |  "
            f"Due Soon: {stats['due_soon']}",
            style="info",
            box=ROUNDED,
        )
        console.print(stats_panel)
        console.print()

        # Menu options
        console.print("  MAIN MENU", style="header")
        console.print("─" * 50, style="divider")

        options = [
            ("📋 View All Tasks", "v", "list"),
            ("➕ Add New Task", "a", "add"),
            ("✏️  Edit Task", "e", "edit"),
            ("✅ Complete Task", "c", "complete"),
            ("🗑️  Delete Task", "d", "delete"),
            ("🔍 Search Tasks", "s", "search"),
            ("🔔 View Reminders", "r", "reminders"),
            ("⚙️  Settings", "g", "settings"),
            ("❌ Exit", "q", "quit"),
        ]

        selected = 0
        while True:
            for i, (text, shortcut, _) in enumerate(options):
                self.print_menu_item(text, i, i == selected, shortcut)

            key = self._get_keypress()

            if key == "up":
                selected = (selected - 1) % len(options)
            elif key == "down":
                selected = (selected + 1) % len(options)
            elif key == "select":
                return options[selected][2]
            elif key == "quit":
                return "quit"

    def _get_task_stats(self) -> dict:
        """Get task statistics for display."""
        tasks = self.service.store.list_all()
        now = self._get_current_datetime()

        return {
            "total": len(tasks),
            "pending": len([t for t in tasks if not t.completed]),
            "completed": len([t for t in tasks if t.completed]),
            "high": len([t for t in tasks if t.priority == Priority.HIGH and not t.completed]),
            "overdue": len([t for t in tasks if self._is_overdue(t, now)]),
            "due_soon": len([t for t in tasks if not t.completed and t.due_date
                           and not self._is_overdue(t, now)
                           and self._is_due_soon(t, now)]),
        }

    def _get_current_datetime(self):
        """Get current datetime for comparisons."""
        from datetime import datetime
        return datetime.now()

    def _is_overdue(self, task: Task, now) -> bool:
        """Check if a task is overdue."""
        if task.completed or not task.due_date:
            return False
        due_datetime = self._get_due_datetime(task)
        return due_datetime < now

    def _is_due_soon(self, task: Task, now) -> bool:
        """Check if a task is due within the reminder threshold."""
        if task.completed or not task.due_date:
            return False
        if self._is_overdue(task, now):
            return False
        due_datetime = self._get_due_datetime(task)
        threshold_end = now + self.config.reminder_threshold
        return now <= due_datetime <= threshold_end

    def _get_due_datetime(self, task: Task):
        """Get task due date/time as datetime."""
        from datetime import datetime
        if task.due_time:
            return datetime.combine(task.due_date, task.due_time)
        return datetime.combine(task.due_date, dt_time(23, 59, 59))

    def _get_keypress(self) -> str:
        """Get a keypress from the user."""
        import sys
        import tty
        import termios

        try:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            tty.setcbreak(sys.stdin.fileno())

            while True:
                ch = sys.stdin.read(1)
                if ch == '\x1b':  # ESC sequence
                    ch = sys.stdin.read(2)
                    if ch == '[A':
                        return "up"
                    elif ch == '[B':
                        return "down"
                    elif ch == '[C':
                        return "right"
                    elif ch == '[D':
                        return "left"
                elif ch == '\n' or ch == '\r':
                    return "select"
                elif ch == 'q' or ch == 'Q':
                    return "quit"
                elif ch == 'a' or ch == 'A':
                    return "add"
                elif ch == 'e' or ch == 'E':
                    return "edit"
                elif ch == 'd' or ch == 'D':
                    return "delete"
                elif ch == 'c' or ch == 'C':
                    return "complete"
                elif ch == 's' or ch == 'S':
                    return "search"
                elif ch == 'r' or ch == 'R':
                    return "reminders"
                elif ch == 'g' or ch == 'G':
                    return "settings"
                elif ch == 'v' or ch == 'V':
                    return "list"
                elif ch == 'h' or ch == 'H':
                    return "help"
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def run(self):
        """Run the main UI loop."""
        console.print(
            Panel(
                Text("Welcome to Todo Extended!", style="title", justify="center"),
                style="cyan",
                subtitle="Press 'q' to quit at any time",
                subtitle_align="center",
            )
        )

        import time
        time.sleep(1.5)

        while self.running:
            result = self.show_main_menu()

            if result == "quit":
                self.running = False
                self.clear_screen()
                console.print(
                    Panel(
                        Text("Goodbye! Thanks for using Todo Extended! 👋", style="title", justify="center"),
                        style="green",
                    )
                )
                break
            elif result == "add":
                self.handle_add()
            elif result == "list":
                self.handle_list()
            elif result == "edit":
                self.handle_edit()
            elif result == "complete":
                self.handle_complete()
            elif result == "delete":
                self.handle_delete()
            elif result == "search":
                self.handle_search()
            elif result == "reminders":
                self.handle_reminders()
            elif result == "settings":
                self.handle_settings()

    def _display_task(self, task: Task, index: int = 0, selected: bool = False):
        """Display a single task with rich styling."""
        # Determine styles based on task state
        if task.completed:
            priority_style = "task_completed"
            status_icon = "[x]"
        else:
            priority_style = f"task_{task.priority.value}"
            status_icon = "[ ]"

        # Build the task display
        parts = []

        # Selection indicator
        if selected:
            parts.append("▶ ")
        else:
            parts.append(f"{index + 1}. ")

        # Priority indicator
        priority_text = f"[{task.priority.value.upper()}]"
        parts.append(f"[{priority_style}]{priority_text}[/] ")

        # Completion status
        parts.append(f"{status_icon} ")

        # Title
        if task.completed:
            parts.append(f"[dim]{task.title}[/]")
        else:
            parts.append(task.title)

        # Tags
        if task.tags:
            tags_str = ", ".join(task.tags)
            parts.append(f" [tag][[tags: {tags_str}]][/]")

        # Due date
        if task.due_date:
            due_str = task.due_date.isoformat()
            if task.due_time:
                due_str += f" {task.due_time.strftime('%H:%M')}"

            # Check if overdue or due soon
            now = self._get_current_datetime()
            if self._is_overdue(task, now):
                parts.append(f" [error][due: {due_str} OVERDUE][/]")
            elif self._is_due_soon(task, now):
                parts.append(f" [prompt][due: {due_str} REMINDER][/]")
            else:
                parts.append(f" [due][due: {due_str}][/]")

        # Recurrence
        if task.recurrence != Recurrence.NONE:
            parts.append(f" [recurring](repeats: {task.recurrence.value})[/]")

        # Render the task line
        task_line = "".join(parts)
        console.print(task_line)

    def handle_add(self):
        """Handle adding a new task."""
        self.clear_screen()
        console.print(Panel(Text("➕ Add New Task", style="header", justify="center"), style="green"))

        try:
            # Get title
            title = Prompt.ask("\n[prompt]Task title[/prompt]")
            if not title.strip():
                self.print_error("Task title cannot be empty")
                return

            # Get description
            description = Prompt.ask("[prompt]Description (optional)[/prompt]", default="")

            # Get priority
            priority_map = {"1": Priority.HIGH, "2": Priority.MEDIUM, "3": Priority.LOW}
            priority_choice = Prompt.ask(
                "[prompt]Priority (1=High, 2=Medium, 3=Low)[/prompt]",
                default="2",
                choices=["1", "2", "3"],
            )
            priority = priority_map[priority_choice]

            # Get tags
            tags_input = Prompt.ask("[prompt]Tags (comma-separated, e.g. work,urgent)[/prompt]", default="")
            tags = []
            if tags_input.strip():
                tags = self.service.validate_tags(tags_input)

            # Get due date
            due_input = Prompt.ask("[prompt]Due date (YYYY-MM-DD, or leave empty)[/prompt]", default="")
            due_date = None
            if due_input.strip():
                due_date = self.service.validate_due_date(due_input)

            # Get recurrence
            recurrence_map = {"1": Recurrence.DAILY, "2": Recurrence.WEEKLY, "3": Recurrence.MONTHLY, "4": Recurrence.NONE}
            recurrence_choice = Prompt.ask(
                "[prompt]Recurrence (1=Daily, 2=Weekly, 3=Monthly, 4=None)[/prompt]",
                default="4",
                choices=["1", "2", "3", "4"],
            )
            recurrence = recurrence_map[recurrence_choice]

            # Create the task
            task = self.service.create_task(
                title=title,
                description=description if description else None,
                priority=priority,
                tags=tags if tags else None,
                due_date=due_date,
                recurrence=recurrence,
            )

            self.print_success(f"Task created successfully!")
            console.print()
            self._display_task(task)

        except ValueError as e:
            self.print_error(str(e))
        except KeyboardInterrupt:
            self.print_info("Cancelled")

        Prompt.ask("\n[info]Press Enter to continue...[/info]")

    def handle_list(self):
        """Handle displaying tasks."""
        self.clear_screen()
        console.print(Panel(Text("📋 Your Tasks", style="header", justify="center"), style="cyan"))

        tasks = self.service.store.list_all()

        if not tasks:
            console.print(Panel(
                Text("No tasks yet!\n\nPress 'a' to add a new task", style="info", justify="center"),
                style="dim",
            ))
            Prompt.ask("\n[info]Press Enter to continue...[/info]")
            return

        # Sort options
        console.print("\n[menu]Sort by:[/menu]")
        console.print("  [1] Creation Date")
        console.print("  [2] Priority")
        console.print("  [3] Due Date")
        console.print("  [4] Title")

        sort_choice = Prompt.ask("[prompt]Choose sort[/prompt]", default="1", choices=["1", "2", "3", "4"])
        sort_map = {"1": "created", "2": "priority", "3": "due_date", "4": "title"}
        tasks = self.service.sort_tasks(tasks, sort_by=sort_map[sort_choice])

        console.print()
        for i, task in enumerate(tasks):
            self._display_task(task, i)

        Prompt.ask("\n[info]Press Enter to continue...[/info]")

    def handle_edit(self):
        """Handle editing a task."""
        self.clear_screen()
        console.print(Panel(Text("✏️ Edit Task", style="header", justify="center"), style="yellow"))

        tasks = self.service.store.list_all()
        if not tasks:
            self.print_info("No tasks to edit")
            Prompt.ask("\n[info]Press Enter to continue...[/info]")
            return

        console.print("\n[info]Available tasks:[/info]")
        for i, task in enumerate(tasks):
            self._display_task(task, i)

        try:
            task_id = int(Prompt.ask("\n[prompt]Enter task ID to edit[/prompt]"))
            task = self.service.get_task(task_id)
        except (ValueError, TypeError):
            self.print_error("Invalid task ID")
            Prompt.ask("\n[info]Press Enter to continue...[/info]")
            return

        console.print(f"\n[info]Editing: {task.title}[/info]")
        console.print("Leave fields blank to keep current value")

        try:
            # Get new title
            new_title = Prompt.ask(f"[prompt]New title (current: {task.title})[/prompt]", default="")
            if not new_title.strip():
                new_title = None

            # Get new description
            current_desc = task.description or ""
            new_desc = Prompt.ask(f"[prompt]New description (current: {current_desc})[/prompt]", default="")
            if not new_desc.strip():
                new_desc = None

            # Get new priority
            console.print(f"[info]Current priority: {task.priority.value}[/info]")
            priority_map = {"1": Priority.HIGH, "2": Priority.MEDIUM, "3": Priority.LOW, "4": "keep"}
            priority_choice = Prompt.ask(
                "[prompt]New priority (1=High, 2=Medium, 3=Low, 4=Keep current)[/prompt]",
                default="4",
                choices=["1", "2", "3", "4"],
            )
            new_priority = priority_map[priority_choice] if priority_choice != "4" else None

            # Get new tags
            current_tags = ", ".join(task.tags) if task.tags else ""
            new_tags_input = Prompt.ask(f"[prompt]New tags (current: {current_tags})[/prompt]", default="")
            new_tags = None
            if new_tags_input.strip():
                new_tags = self.service.validate_tags(new_tags_input)

            # Update the task
            updated = self.service.update_task(
                task_id=task_id,
                title=new_title,
                description=new_desc,
                priority=new_priority,
                tags=new_tags,
            )

            self.print_success("Task updated successfully!")
            console.print()
            self._display_task(updated)

        except ValueError as e:
            self.print_error(str(e))
        except KeyboardInterrupt:
            self.print_info("Cancelled")

        Prompt.ask("\n[info]Press Enter to continue...[/info]")

    def handle_complete(self):
        """Handle completing a task."""
        self.clear_screen()
        console.print(Panel(Text("✅ Complete Task", style="header", justify="center"), style="green"))

        tasks = [t for t in self.service.store.list_all() if not t.completed]
        if not tasks:
            console.print(Panel(
                Text("All tasks are already completed! 🎉", style="success", justify="center"),
                style="green",
            ))
            Prompt.ask("\n[info]Press Enter to continue...[/info]")
            return

        console.print("\n[info]Pending tasks:[/info]")
        for i, task in enumerate(tasks):
            self._display_task(task, i)

        try:
            task_id = int(Prompt.ask("\n[prompt]Enter task ID to complete[/prompt]"))
            task, new_task = self.service.complete_task(task_id)

            self.print_success(f"Task completed!")
            if new_task:
                console.print()
                self.print_info("New recurring task created:")
                self._display_task(new_task)

        except ValueError as e:
            self.print_error(str(e))

        Prompt.ask("\n[info]Press Enter to continue...[/info]")

    def handle_delete(self):
        """Handle deleting a task."""
        self.clear_screen()
        console.print(Panel(Text("🗑️ Delete Task", style="header", justify="center"), style="red"))

        tasks = self.service.store.list_all()
        if not tasks:
            self.print_info("No tasks to delete")
            Prompt.ask("\n[info]Press Enter to continue...[/info]")
            return

        console.print("\n[info]All tasks:[/info]")
        for i, task in enumerate(tasks):
            self._display_task(task, i)

        try:
            task_id = int(Prompt.ask("\n[prompt]Enter task ID to delete[/prompt]"))

            if Confirm.ask(f"[error]Are you sure you want to delete task {task_id}?[/error]"):
                self.service.delete_task(task_id)
                self.print_success("Task deleted")
            else:
                self.print_info("Deletion cancelled")

        except ValueError as e:
            self.print_error(str(e))

        Prompt.ask("\n[info]Press Enter to continue...[/info]")

    def handle_search(self):
        """Handle searching for tasks."""
        self.clear_screen()
        console.print(Panel(Text("🔍 Search Tasks", style="header", justify="center"), style="cyan"))

        keyword = Prompt.ask("\n[prompt]Enter search keyword[/prompt]")

        if not keyword.strip():
            self.print_info("No keyword entered")
            Prompt.ask("\n[info]Press Enter to continue...[/info]")
            return

        tasks = self.service.search_tasks(keyword)

        if not tasks:
            self.print_info(f"No tasks found matching '{keyword}'")
        else:
            console.print(f"\n[success]Found {len(tasks)} task(s):[/success]")
            for i, task in enumerate(tasks):
                self._display_task(task, i)

        Prompt.ask("\n[info]Press Enter to continue...[/info]")

    def handle_reminders(self):
        """Handle viewing reminder/overdue tasks."""
        self.clear_screen()
        console.print(Panel(Text("🔔 Reminders & Overdue", style="header", justify="center"), style="orange3"))

        tasks = self.service.get_reminder_tasks()

        if not tasks:
            console.print(Panel(
                Text("No tasks requiring attention!\n\nYou're all caught up! 🎉", style="success", justify="center"),
                style="green",
            ))
        else:
            console.print(f"\n[error]{len(tasks)} task(s) need attention:[/error]")
            for i, task in enumerate(tasks):
                self._display_task(task, i)

        Prompt.ask("\n[info]Press Enter to continue...[/info]")

    def handle_settings(self):
        """Handle settings."""
        self.clear_screen()
        console.print(Panel(Text("⚙️ Settings", style="header", justify="center"), style="magenta"))

        console.print(f"\n[info]Current reminder threshold: {self.config.get_threshold_display()}[/info]")

        console.print("\n[menu]Available options:[/menu]")
        console.print("  [1] Set reminder threshold")
        console.print("  [2] View all settings")
        console.print("  [3] Back to main menu")

        choice = Prompt.ask("[prompt]Choose option[/prompt]", default="3", choices=["1", "2", "3"])

        if choice == "1":
            new_threshold = Prompt.ask("[prompt]Enter new threshold (e.g., 12h, 24h, 7d)[/prompt]")
            try:
                self.config.set_threshold(new_threshold)
                self.print_success(f"Reminder threshold set to {new_threshold}")
            except ValueError as e:
                self.print_error(str(e))
        elif choice == "2":
            console.print(format_config({
                "reminder_threshold": self.config.get_threshold_display(),
            }))

        Prompt.ask("\n[info]Press Enter to continue...[/info]")


def format_config(settings: dict) -> str:
    """Format configuration display."""
    lines = ["Current settings:"]
    for key, value in settings.items():
        lines.append(f"- {key}: {value}")
    return "\n".join(lines)


def run_ui():
    """Entry point for the interactive UI."""
    ui = TodoUI()
    ui.run()


if __name__ == "__main__":
    run_ui()
