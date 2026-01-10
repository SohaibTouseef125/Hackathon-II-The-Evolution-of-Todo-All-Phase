"""Unit tests for recurrence calculation logic."""

import pytest
from datetime import date

from src.models.task import Recurrence
from src.services.recurrence import calculate_next_due_date


class TestRecurrenceCalculation:
    """Tests for calculate_next_due_date function."""

    def test_daily_recurrence(self):
        """Daily recurrence adds 1 day."""
        current = date(2025, 1, 15)
        result = calculate_next_due_date(current, Recurrence.DAILY)
        assert result == date(2025, 1, 16)

    def test_weekly_recurrence(self):
        """Weekly recurrence adds 7 days."""
        current = date(2025, 1, 15)
        result = calculate_next_due_date(current, Recurrence.WEEKLY)
        assert result == date(2025, 1, 22)

    def test_monthly_recurrence_normal(self):
        """Monthly recurrence adds 1 month (same day)."""
        current = date(2025, 1, 15)
        result = calculate_next_due_date(current, Recurrence.MONTHLY)
        assert result == date(2025, 2, 15)

    def test_monthly_recurrence_jan31_to_feb28(self):
        """Jan 31 -> Feb 28 (non-leap year)."""
        current = date(2025, 1, 31)
        result = calculate_next_due_date(current, Recurrence.MONTHLY)
        assert result == date(2025, 2, 28)

    def test_monthly_recurrence_jan31_to_feb29_leap_year(self):
        """Jan 31 -> Feb 29 (leap year)."""
        current = date(2024, 1, 31)
        result = calculate_next_due_date(current, Recurrence.MONTHLY)
        assert result == date(2024, 2, 29)

    def test_monthly_recurrence_jan30_to_feb28(self):
        """Jan 30 -> Feb 28 (non-leap year)."""
        current = date(2025, 1, 30)
        result = calculate_next_due_date(current, Recurrence.MONTHLY)
        assert result == date(2025, 2, 28)

    def test_monthly_recurrence_mar31_to_apr30(self):
        """Mar 31 -> Apr 30 (April has 30 days)."""
        current = date(2025, 3, 31)
        result = calculate_next_due_date(current, Recurrence.MONTHLY)
        assert result == date(2025, 4, 30)

    def test_monthly_recurrence_dec_to_jan(self):
        """Dec 15 -> Jan 15 (year rollover)."""
        current = date(2025, 12, 15)
        result = calculate_next_due_date(current, Recurrence.MONTHLY)
        assert result == date(2026, 1, 15)

    def test_monthly_recurrence_dec31_to_jan31(self):
        """Dec 31 -> Jan 31 (year rollover, same day)."""
        current = date(2025, 12, 31)
        result = calculate_next_due_date(current, Recurrence.MONTHLY)
        assert result == date(2026, 1, 31)

    def test_none_recurrence_raises(self):
        """NONE recurrence should raise ValueError."""
        with pytest.raises(ValueError, match="non-recurring"):
            calculate_next_due_date(date(2025, 1, 15), Recurrence.NONE)

    def test_multiple_monthly_increments(self):
        """Test several months of monthly recurrence."""
        d = date(2025, 1, 31)

        # Jan 31 -> Feb 28
        d = calculate_next_due_date(d, Recurrence.MONTHLY)
        assert d == date(2025, 2, 28)

        # Feb 28 -> Mar 28 (not 31, because we started with 28)
        d = calculate_next_due_date(d, Recurrence.MONTHLY)
        assert d == date(2025, 3, 28)

        # Mar 28 -> Apr 28
        d = calculate_next_due_date(d, Recurrence.MONTHLY)
        assert d == date(2025, 4, 28)
