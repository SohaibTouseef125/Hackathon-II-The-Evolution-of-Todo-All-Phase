"""Recurrence calculation logic.

This module provides functions for calculating next due dates for recurring tasks.
"""

from calendar import monthrange
from datetime import date, timedelta

from src.models.task import Recurrence


def calculate_next_due_date(current_date: date, pattern: Recurrence) -> date:
    """Calculate the next due date based on recurrence pattern.

    Args:
        current_date: Current due date
        pattern: Recurrence pattern

    Returns:
        Next due date

    Raises:
        ValueError: If pattern is NONE
    """
    if pattern == Recurrence.NONE:
        raise ValueError("Cannot calculate next due date for non-recurring task")

    if pattern == Recurrence.DAILY:
        return current_date + timedelta(days=1)

    elif pattern == Recurrence.WEEKLY:
        return current_date + timedelta(days=7)

    elif pattern == Recurrence.MONTHLY:
        return _add_one_month(current_date)

    raise ValueError(f"Unknown recurrence pattern: {pattern}")


def _add_one_month(d: date) -> date:
    """Add one month to a date, handling edge cases.

    If the target day doesn't exist in the next month, clamp to the last day.
    Examples:
        - Jan 15 -> Feb 15
        - Jan 31 -> Feb 28 (or Feb 29 in leap year)
        - Mar 31 -> Apr 30

    Args:
        d: Source date

    Returns:
        Date one month later
    """
    # Calculate next month
    if d.month == 12:
        next_year = d.year + 1
        next_month = 1
    else:
        next_year = d.year
        next_month = d.month + 1

    # Get the last day of the next month
    max_day = monthrange(next_year, next_month)[1]

    # Clamp the day if it exceeds the max
    day = min(d.day, max_day)

    return date(next_year, next_month, day)
