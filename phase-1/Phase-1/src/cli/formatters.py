"""Output formatting for CLI display.

This module provides functions for formatting tasks and messages for CLI output.
"""

from typing import List, Optional

from src.models.task import Task, Recurrence
from src.services.task_service import TaskService


def format_task(
    task: Task,
    service: Optional[TaskService] = None,
    show_id: bool = True,
) -> str:
    """Format a single task for display.

    Format: [ID]. [OVERDUE/REMINDER] [PRIORITY] [x/] Title (repeats: pattern) [due: date time] [tags: t1, t2]

    Args:
        task: Task to format
        service: Optional TaskService for checking overdue/reminder status
        show_id: Whether to show task ID

    Returns:
        Formatted task string
    """
    parts = []

    # Task ID
    if show_id:
        parts.append(f"{task.id}.")

    # Status indicators (order matters: OVERDUE first, then REMINDER)
    if service:
        if service.is_overdue(task):
            parts.append("[OVERDUE]")
        elif service.is_reminder(task):
            parts.append("[REMINDER]")

    # Priority
    parts.append(f"[{task.priority.value.upper()}]")

    # Completion status
    parts.append("[x]" if task.completed else "[ ]")

    # Title
    parts.append(task.title)

    # Recurrence
    if task.recurrence != Recurrence.NONE:
        parts.append(f"(repeats: {task.recurrence.value})")

    # Due date/time
    if task.due_date:
        due_str = task.due_date.isoformat()
        if task.due_time:
            due_str += f" {task.due_time.strftime('%H:%M')}"
        parts.append(f"[due: {due_str}]")

    # Tags
    if task.tags:
        parts.append(f"[tags: {', '.join(task.tags)}]")

    return " ".join(parts)


def format_task_list(
    tasks: List[Task],
    service: Optional[TaskService] = None,
    header: Optional[str] = None,
) -> str:
    """Format a list of tasks for display.

    Args:
        tasks: List of tasks to format
        service: Optional TaskService for checking overdue/reminder status
        header: Optional header to display before list

    Returns:
        Formatted task list string
    """
    if not tasks:
        return "No tasks to display"

    lines = []

    if header:
        lines.append(f"{header} ({len(tasks)}):")

    for task in tasks:
        lines.append(format_task(task, service))

    return "\n".join(lines)


def format_task_created(task: Task) -> str:
    """Format task creation message.

    Args:
        task: Created task

    Returns:
        Creation message string
    """
    return f"Task {task.id} created: {format_task(task, show_id=False)}"


def format_task_updated(task: Task) -> str:
    """Format task update message.

    Args:
        task: Updated task

    Returns:
        Update message string
    """
    return f"Task {task.id} updated: {format_task(task, show_id=False)}"


def format_task_deleted(task_id: int) -> str:
    """Format task deletion message.

    Args:
        task_id: Deleted task ID

    Returns:
        Deletion message string
    """
    return f"Task {task_id} deleted"


def format_task_completed(task: Task, new_task: Optional[Task] = None) -> str:
    """Format task completion message.

    Args:
        task: Completed task
        new_task: New recurring task if created

    Returns:
        Completion message string
    """
    lines = [f"Task {task.id} completed: {format_task(task, show_id=False)}"]

    if new_task:
        lines.append("New recurring task created:")
        lines.append(f"Task {new_task.id}: {format_task(new_task, show_id=False)}")

    return "\n".join(lines)


def format_search_results(tasks: List[Task], keyword: str) -> str:
    """Format search results.

    Args:
        tasks: List of matching tasks
        keyword: Search keyword

    Returns:
        Formatted search results string
    """
    if not tasks:
        return f"No tasks found matching '{keyword}'"

    lines = [f"Found {len(tasks)} tasks matching '{keyword}':"]
    for task in tasks:
        lines.append(format_task(task))

    return "\n".join(lines)


def format_filter_results(
    tasks: List[Task],
    service: Optional[TaskService] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    due: Optional[str] = None,
) -> str:
    """Format filtered task list.

    Args:
        tasks: List of filtered tasks
        service: Optional TaskService for status indicators
        status: Filter status
        priority: Filter priority
        due: Filter due date

    Returns:
        Formatted filter results string
    """
    if not tasks:
        return "No tasks match the specified filters"

    # Build header
    filter_parts = []
    if status and status != "all":
        filter_parts.append(status.capitalize())
    if priority and priority != "all":
        filter_parts.append(f"{priority}-priority")
    if due and due != "all":
        filter_parts.append(f"due {due}")

    if filter_parts:
        header = " ".join(filter_parts) + " tasks"
    else:
        header = "All tasks"

    return format_task_list(tasks, service, header)


def format_reminder_list(tasks: List[Task], service: TaskService) -> str:
    """Format reminder tasks list.

    Args:
        tasks: List of reminder/overdue tasks
        service: TaskService for status indicators

    Returns:
        Formatted reminder list string
    """
    if not tasks:
        return "No tasks requiring attention"

    return format_task_list(tasks, service, "Tasks requiring attention")


def format_config(settings: dict) -> str:
    """Format configuration display.

    Args:
        settings: Dictionary of settings

    Returns:
        Formatted settings string
    """
    lines = ["Current settings:"]
    for key, value in settings.items():
        lines.append(f"- {key}: {value}")
    return "\n".join(lines)


def format_error(message: str) -> str:
    """Format error message.

    Args:
        message: Error message

    Returns:
        Formatted error string
    """
    return f"Error: {message}"
