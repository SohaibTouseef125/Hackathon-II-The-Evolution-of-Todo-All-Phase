# Research: Phase 1 Extended Features

**Feature Branch**: `002-phase1-extended`
**Date**: 2025-12-29
**Status**: Complete

---

## Research Questions

### 1. Date/Time Handling in Python

**Question**: Best approach for date/time handling in Phase 1 (in-memory, no persistence)?

**Decision**: Use Python's built-in `datetime` module with `date` and `time` classes.

**Rationale**:
- No external dependencies required (constitution compliance)
- Built-in ISO format parsing (`datetime.fromisoformat()`)
- Native date arithmetic with `timedelta` and `relativedelta` patterns
- System local timezone via `datetime.now()`

**Alternatives Considered**:
- `arrow` library: Rejected (external dependency, not needed for basic operations)
- `pendulum` library: Rejected (overkill for Phase 1 scope)
- Manual string parsing: Rejected (error-prone, reinventing the wheel)

---

### 2. CLI Argument Parsing

**Question**: How to handle extended CLI flags (`--priority`, `--tags`, `--due`, `--sort`, etc.)?

**Decision**: Extend existing `argparse` implementation with subcommand-specific optional arguments.

**Rationale**:
- Already using argparse for Basic Level features
- Native support for optional arguments, defaults, choices
- Type validation built-in
- Help text generation automatic

**Alternatives Considered**:
- `click` library: Rejected (external dependency)
- `typer` library: Rejected (external dependency)
- Custom parsing: Rejected (reinventing argparse)

---

### 3. Enum Implementation for Priority/Recurrence

**Question**: How to implement enum types for `priority` and `recurrence`?

**Decision**: Use Python's built-in `enum.Enum` class with string values.

**Rationale**:
- Built-in, no dependencies
- Type safety with IDE support
- String values for CLI compatibility
- Easy comparison and validation

**Implementation Pattern**:
```python
from enum import Enum

class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Recurrence(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    NONE = "none"
```

---

### 4. Monthly Recurrence Edge Cases

**Question**: How to handle monthly recurrence when target day doesn't exist (e.g., Jan 31 → Feb)?

**Decision**: Use "last day of month" strategy when day overflow occurs.

**Rationale**:
- Most intuitive for users (Jan 31 → Feb 28/29 → Mar 31)
- Standard calendar library behavior
- Preserves "end of month" intent

**Implementation**:
```python
from calendar import monthrange

def add_one_month(date):
    year = date.year + (date.month // 12)
    month = (date.month % 12) + 1
    max_day = monthrange(year, month)[1]
    day = min(date.day, max_day)
    return date.replace(year=year, month=month, day=day)
```

---

### 5. Search Algorithm

**Question**: Best approach for case-insensitive substring search?

**Decision**: Simple `in` operator with `.lower()` normalization.

**Rationale**:
- O(n) per task, O(n*m) total - acceptable for in-memory lists up to 1000 tasks
- No indexing overhead
- Matches title AND description

**Implementation Pattern**:
```python
def search_tasks(tasks, keyword):
    keyword_lower = keyword.lower()
    return [t for t in tasks if
            keyword_lower in t.title.lower() or
            keyword_lower in (t.description or "").lower()]
```

---

### 6. Sorting Strategy

**Question**: How to implement multi-criteria sorting with null handling?

**Decision**: Use `sorted()` with custom key functions and tuple-based ordering.

**Rationale**:
- Python's timsort is stable (preserves original order for equal elements)
- Tuple comparison handles multiple criteria naturally
- None values can be sorted to end using sentinel values

**Implementation Pattern**:
```python
def sort_by_due_date(tasks, reverse=False):
    # None values go to end (use max date as sentinel)
    sentinel = date.max if not reverse else date.min
    return sorted(tasks,
                  key=lambda t: t.due_date or sentinel,
                  reverse=reverse)
```

---

### 7. Tag Storage and Validation

**Question**: How to store and validate tags?

**Decision**: List of lowercase strings with validation on input.

**Rationale**:
- Case-insensitive storage (normalized to lowercase)
- Deduplication on input
- Simple list operations for add/remove
- Comma-separated input parsing

**Validation Rules**:
- Max 50 characters per tag
- Alphanumeric, hyphens, underscores only
- No empty strings or whitespace-only
- Auto-deduplicate

---

### 8. Reminder Threshold Configuration

**Question**: How to implement configurable reminder threshold?

**Decision**: Simple in-memory configuration object with duration parsing.

**Rationale**:
- No persistence needed (Phase 1 constraint)
- Duration string format (`1h`, `24h`, `7d`) is user-friendly
- Default to 24 hours

**Implementation Pattern**:
```python
class Config:
    def __init__(self):
        self.reminder_threshold = timedelta(hours=24)

    def parse_threshold(self, value):
        # Parse "1h", "24h", "7d" format
        if value.endswith('h'):
            return timedelta(hours=int(value[:-1]))
        elif value.endswith('d'):
            return timedelta(days=int(value[:-1]))
```

---

## Dependencies Analysis

### Required (Built-in Python)

| Module | Purpose | Risk |
|--------|---------|------|
| `datetime` | Date/time operations | None (built-in) |
| `enum` | Priority/Recurrence types | None (built-in) |
| `argparse` | CLI parsing | None (built-in) |
| `calendar` | Month calculations | None (built-in) |
| `re` | Tag validation regex | None (built-in) |

### Not Required (Rejected External)

| Library | Reason for Rejection |
|---------|---------------------|
| `arrow` | External dependency, overkill |
| `dateutil` | External dependency |
| `click` | External dependency |
| `pendulum` | External dependency |

---

## Risk Assessment

### Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Performance with 1000+ tasks | Low | Medium | In-memory operations are fast; test at scale |
| Timezone edge cases | Medium | Low | Use local time consistently; document assumption |
| Monthly recurrence bugs | Medium | Medium | Comprehensive test cases for edge dates |

### Scope Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Feature creep | Medium | High | Strict adherence to spec; reject unspec'd features |
| Overengineering | Medium | Medium | Follow YAGNI; minimal viable implementation |

---

## Conclusion

All technical questions resolved. No external dependencies required. Implementation can proceed with Python built-in modules only:
- `datetime`, `timedelta` for date operations
- `enum.Enum` for type safety
- `argparse` for CLI (already in use)
- `calendar` for month calculations

Ready for Phase 1: Design & Contracts.
