# Data Model: Phase 1 Extended Features

**Feature Branch**: `002-phase1-extended`
**Date**: 2025-12-29
**Status**: Complete

---

## Entity Definitions

### Task (Extended)

The Task entity extends the Basic Level model with additional fields for organization and automation.

#### Schema

```python
@dataclass
class Task:
    # Basic Level (existing)
    id: int                          # Auto-incremented unique identifier
    title: str                       # Required, 1-200 characters
    description: Optional[str]       # Optional, max 1000 characters
    completed: bool                  # Default: False
    created_at: datetime             # Auto-set on creation
    updated_at: datetime             # Auto-set on update

    # Intermediate Level (new)
    priority: Priority               # Default: Priority.MEDIUM
    tags: List[str]                  # Default: []

    # Advanced Level (new)
    due_date: Optional[date]         # Optional, YYYY-MM-DD format
    due_time: Optional[time]         # Optional, HH:MM format (requires due_date)
    recurrence: Recurrence           # Default: Recurrence.NONE
```

#### Field Specifications

| Field | Type | Required | Default | Constraints | Validation |
|-------|------|----------|---------|-------------|------------|
| id | int | Yes | auto | Positive integer, unique | Auto-generated |
| title | str | Yes | - | 1-200 chars | Non-empty, trimmed |
| description | str | No | None | Max 1000 chars | Trimmed if present |
| completed | bool | Yes | False | - | Boolean |
| created_at | datetime | Yes | now() | Immutable after creation | Auto-set |
| updated_at | datetime | Yes | now() | Updates on any change | Auto-set |
| priority | Priority | Yes | MEDIUM | Enum value | Valid enum |
| tags | List[str] | No | [] | Max 10 tags, 50 chars each | Lowercase, deduplicated |
| due_date | date | No | None | YYYY-MM-DD | Today or future |
| due_time | time | No | None | HH:MM (24h) | Requires due_date |
| recurrence | Recurrence | Yes | NONE | Enum value | Requires due_date if not NONE |

---

### Priority Enum

```python
class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    @classmethod
    def from_string(cls, value: str) -> 'Priority':
        """Parse string to Priority, case-insensitive."""
        return cls(value.lower())

    def sort_key(self) -> int:
        """Return numeric value for sorting (high=1, medium=2, low=3)."""
        return {"high": 1, "medium": 2, "low": 3}[self.value]
```

#### Priority Sort Order

| Priority | Sort Key | Display |
|----------|----------|---------|
| HIGH | 1 | `[HIGH]` |
| MEDIUM | 2 | `[MEDIUM]` |
| LOW | 3 | `[LOW]` |

---

### Recurrence Enum

```python
class Recurrence(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    NONE = "none"

    @classmethod
    def from_string(cls, value: str) -> 'Recurrence':
        """Parse string to Recurrence, case-insensitive."""
        return cls(value.lower())
```

#### Recurrence Calculation Rules

| Pattern | Calculation | Edge Case Handling |
|---------|-------------|-------------------|
| DAILY | due_date + 1 day | None |
| WEEKLY | due_date + 7 days | None |
| MONTHLY | due_date + 1 month | Clamp to last day of month |
| NONE | No recurrence | N/A |

---

### Configuration

Global configuration for the application (in-memory, per-session).

```python
@dataclass
class Config:
    reminder_threshold: timedelta = timedelta(hours=24)

    def set_threshold(self, value: str) -> None:
        """Parse and set threshold from string like '24h', '7d'."""
        pass

    def get_threshold_display(self) -> str:
        """Return human-readable threshold string."""
        pass
```

#### Configuration Fields

| Setting | Type | Default | Valid Values | Description |
|---------|------|---------|--------------|-------------|
| reminder_threshold | timedelta | 24h | 1h, 6h, 12h, 24h, 48h, 7d | Time before due to show reminder |

---

## State Transitions

### Task Completion State

```
┌──────────┐    complete()    ┌───────────┐
│ PENDING  │ ───────────────> │ COMPLETED │
│completed │                   │completed  │
│ = false  │ <─────────────── │ = true    │
└──────────┘   uncomplete()   └───────────┘
                                    │
                                    │ (if recurrence != NONE)
                                    ▼
                              ┌───────────┐
                              │ NEW TASK  │
                              │ PENDING   │
                              │ due_date  │
                              │ = next    │
                              └───────────┘
```

### Recurrence Trigger

When `complete()` is called on a task with `recurrence != NONE`:

1. Mark current task as `completed = True`
2. Calculate next due date based on recurrence pattern
3. Create new task with:
   - New auto-generated ID
   - Same title, description, priority, tags, recurrence
   - `completed = False`
   - `due_date = calculated_next_date`
   - `due_time = original_due_time` (preserved if set)
   - `created_at = now()`
   - `updated_at = now()`

---

## Relationships

### Entity Relationship Diagram

```
┌─────────────────────────────────────────────────┐
│                     TASK                         │
├─────────────────────────────────────────────────┤
│ PK  id: int                                      │
│     title: str                                   │
│     description: str?                            │
│     completed: bool                              │
│     priority: Priority                           │
│     tags: List[str]                              │
│     due_date: date?                              │
│     due_time: time?                              │
│     recurrence: Recurrence                       │
│     created_at: datetime                         │
│     updated_at: datetime                         │
└─────────────────────────────────────────────────┘
                      │
                      │ 1:1 (per session)
                      ▼
┌─────────────────────────────────────────────────┐
│                   CONFIG                         │
├─────────────────────────────────────────────────┤
│     reminder_threshold: timedelta                │
└─────────────────────────────────────────────────┘
```

### Storage Structure

```python
class TaskStore:
    """In-memory task storage."""

    def __init__(self):
        self.tasks: Dict[int, Task] = {}  # id -> Task mapping
        self.next_id: int = 1             # Auto-increment counter
        self.config: Config = Config()     # Global configuration

    def add(self, task: Task) -> Task:
        """Add task, assign ID, return created task."""
        pass

    def get(self, id: int) -> Optional[Task]:
        """Get task by ID."""
        pass

    def update(self, id: int, **fields) -> Task:
        """Update task fields, return updated task."""
        pass

    def delete(self, id: int) -> bool:
        """Delete task by ID, return success."""
        pass

    def list_all(self) -> List[Task]:
        """Return all tasks."""
        pass
```

---

## Validation Rules

### Task Title
- Required (cannot be empty or whitespace only)
- Length: 1-200 characters after trimming
- Error: "Task title is required" / "Task title must be 200 characters or less"

### Task Description
- Optional (can be None or empty string)
- Length: 0-1000 characters after trimming
- Error: "Task description must be 1000 characters or less"

### Priority
- Must be valid enum value: high, medium, low
- Case-insensitive input
- Error: "Invalid priority. Use: high, medium, low"

### Tags
- Each tag: 1-50 alphanumeric characters, hyphens, underscores
- Maximum 10 tags per task
- Auto-normalize: lowercase, deduplicate, trim whitespace
- Regex: `^[a-zA-Z0-9_-]+$`
- Error: "Invalid tag format" / "Maximum 10 tags allowed"

### Due Date
- Format: YYYY-MM-DD (ISO 8601)
- Must be today or in the future
- Error: "Invalid date format. Use YYYY-MM-DD" / "Due date cannot be in the past"

### Due Time
- Format: HH:MM (24-hour)
- Requires due_date to be set
- Range: 00:00 to 23:59
- Error: "Invalid time format. Use HH:MM" / "Due time requires a due date"

### Recurrence
- Must be valid enum value: daily, weekly, monthly, none
- Requires due_date if not "none"
- Error: "Recurring tasks must have a due date"

### Reminder Threshold
- Format: `<number>h` or `<number>d`
- Valid values: 1h, 6h, 12h, 24h, 48h, 7d
- Error: "Invalid threshold format. Use: 1h, 6h, 12h, 24h, 48h, 7d"

---

## Computed Properties

### Task Status Indicators

```python
@property
def is_overdue(self) -> bool:
    """True if task has due date in the past and not completed."""
    if self.completed or not self.due_date:
        return False
    due_datetime = self._get_due_datetime()
    return due_datetime < datetime.now()

@property
def is_reminder(self) -> bool:
    """True if task is due within reminder threshold."""
    if self.completed or not self.due_date or self.is_overdue:
        return False
    due_datetime = self._get_due_datetime()
    threshold = config.reminder_threshold
    return datetime.now() <= due_datetime <= datetime.now() + threshold

def _get_due_datetime(self) -> datetime:
    """Combine due_date and due_time into datetime."""
    if self.due_time:
        return datetime.combine(self.due_date, self.due_time)
    return datetime.combine(self.due_date, time(23, 59, 59))
```

### Display Format

```python
def format_display(self) -> str:
    """Return formatted task string for CLI display."""
    parts = []

    # Status indicators (order matters)
    if self.is_overdue:
        parts.append("[OVERDUE]")
    elif self.is_reminder:
        parts.append("[REMINDER]")

    # Priority
    parts.append(f"[{self.priority.value.upper()}]")

    # Completion status
    parts.append("[x]" if self.completed else "[ ]")

    # Title
    parts.append(self.title)

    # Recurrence
    if self.recurrence != Recurrence.NONE:
        parts.append(f"(repeats: {self.recurrence.value})")

    # Due date/time
    if self.due_date:
        due_str = self.due_date.isoformat()
        if self.due_time:
            due_str += f" {self.due_time.strftime('%H:%M')}"
        parts.append(f"[due: {due_str}]")

    # Tags
    if self.tags:
        parts.append(f"[tags: {', '.join(self.tags)}]")

    return " ".join(parts)
```

**Example Outputs**:
```
[HIGH] [ ] Finish report [tags: work, urgent]
[REMINDER] [MEDIUM] [ ] Team meeting [due: 2025-12-30 14:30]
[OVERDUE] [HIGH] [ ] Submit proposal [due: 2025-12-28]
[LOW] [x] Buy groceries (repeats: weekly) [due: 2025-12-31]
```
