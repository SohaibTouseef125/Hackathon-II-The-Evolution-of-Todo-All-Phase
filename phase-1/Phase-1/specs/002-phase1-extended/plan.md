# Implementation Plan: Phase 1 Extended Features

**Branch**: `002-phase1-extended` | **Date**: 2025-12-29 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-phase1-extended/spec.md`

---

## Summary

Extend the Phase 1 Todo Console Application with **Intermediate Level** (Priorities, Tags, Search, Filter, Sort) and **Advanced Level** (Recurring Tasks, Due Dates & Reminders) features. All implementation uses Python built-in modules only (datetime, enum, argparse, calendar) with in-memory storage and CLI interface.

**Total Scope**: 5 features, 47 functional requirements, 17 user stories

---

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Built-in only (argparse, datetime, enum, calendar, re)
**Storage**: In-memory (Dict[int, Task])
**Testing**: unittest (Python built-in)
**Target Platform**: CLI / Console
**Project Type**: Single project
**Performance Goals**: All commands < 1 second for up to 1000 tasks
**Constraints**: No external dependencies, no database, no background workers
**Scale/Scope**: Single user, session-based persistence

---

## Constitution Check

*GATE: Passed - All requirements comply with Phase 1 Constitution v1.1.0*

| Gate | Status | Notes |
|------|--------|-------|
| Python 3.13+ | ✅ | Using built-in modules only |
| No external dependencies | ✅ | datetime, enum, argparse, calendar, re all built-in |
| In-memory storage | ✅ | Dict[int, Task] pattern |
| CLI interface | ✅ | argparse with subcommands |
| TDD mandatory | ✅ | unittest with Red-Green-Refactor |
| No background workers | ✅ | All operations synchronous |
| UV package manager | ✅ | Project setup requirement |

---

## Project Structure

### Documentation (this feature)

```text
specs/002-phase1-extended/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file
├── research.md          # Technical research (complete)
├── data-model.md        # Entity definitions (complete)
├── checklists/
│   └── requirements.md  # Requirements checklist (complete)
└── tasks.md             # Implementation tasks (pending /sp.tasks)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── main.py              # CLI entry point
├── models/
│   ├── __init__.py
│   ├── task.py          # Task dataclass with Priority, Recurrence enums
│   └── config.py        # Configuration dataclass
├── services/
│   ├── __init__.py
│   ├── task_store.py    # In-memory task storage
│   ├── task_service.py  # Business logic (CRUD, complete, search, filter, sort)
│   └── recurrence.py    # Recurrence calculation logic
└── cli/
    ├── __init__.py
    ├── parser.py        # argparse setup with all subcommands
    ├── commands.py      # Command handlers
    └── formatters.py    # Output formatting (display strings)

tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_models.py       # Task, Priority, Recurrence, Config tests
│   ├── test_task_store.py   # Storage CRUD tests
│   ├── test_task_service.py # Business logic tests
│   ├── test_recurrence.py   # Recurrence calculation tests
│   └── test_formatters.py   # Display format tests
├── integration/
│   ├── __init__.py
│   └── test_cli.py          # End-to-end CLI tests
└── contract/
    ├── __init__.py
    └── test_validation.py   # Input validation contract tests
```

**Structure Decision**: Single project layout selected per Phase 1 constraints. Models, services, and CLI are separated for testability while maintaining simplicity.

---

## Complexity Tracking

> No violations - all requirements comply with constitution.

---

## Implementation Phases

### Phase 1: Core Models & Enums

**Objective**: Define data structures for extended features

**Components**:
1. `Priority` enum (high, medium, low) with sort_key method
2. `Recurrence` enum (daily, weekly, monthly, none)
3. Extended `Task` dataclass with new fields:
   - priority: Priority (default: MEDIUM)
   - tags: List[str] (default: [])
   - due_date: Optional[date]
   - due_time: Optional[time]
   - recurrence: Recurrence (default: NONE)
4. `Config` dataclass with reminder_threshold

**Validation Rules**:
- Title: 1-200 chars, non-empty after trim
- Description: 0-1000 chars
- Tags: max 10 tags, each 1-50 chars, alphanumeric/hyphen/underscore
- Due date: today or future, YYYY-MM-DD format
- Due time: requires due_date, HH:MM format
- Recurrence: requires due_date if not NONE

**Test Strategy**: Unit tests for each enum, validation, and computed property

---

### Phase 2: Priority & Tags (Intermediate Level - Feature 1)

**Objective**: Enable task organization by importance and category

**CLI Commands**:
```bash
# Add with priority and tags
todo add "Task title" --priority high --tags work,urgent

# Update priority
todo update <id> --priority low

# Update tags
todo update <id> --tags home,shopping
```

**Implementation Steps**:
1. Add `--priority` argument to `add` and `update` subcommands
2. Add `--tags` argument (comma-separated) to `add` and `update`
3. Update `Task.format_display()` to show `[PRIORITY]` and `[tags: ...]`
4. Add tag parsing/validation (lowercase, dedupe, max 10)
5. Update task store to handle new fields

**Acceptance Tests**:
- [ ] Priority set at creation
- [ ] Priority defaults to medium
- [ ] Priority updateable
- [ ] Tags set at creation (comma-separated)
- [ ] Tags updateable (replace)
- [ ] Tags deduplicated and lowercased
- [ ] Invalid priority shows error
- [ ] Invalid tag format shows error

---

### Phase 3: Search & Filter (Intermediate Level - Feature 2)

**Objective**: Enable efficient task discovery

**CLI Commands**:
```bash
# Search by keyword
todo search "report"

# Filter by status
todo list --status pending|completed|all

# Filter by priority
todo list --priority high|medium|low|all

# Filter by due date
todo list --due today|week|overdue|all

# Combined filters
todo list --status pending --priority high --due week
```

**Implementation Steps**:
1. Add `search` subcommand with keyword argument
2. Implement case-insensitive substring search in title and description
3. Add `--status`, `--priority`, `--due` filter arguments to `list`
4. Implement filter logic in TaskService
5. Display result count

**Filter Logic**:
```python
def filter_tasks(tasks, status=None, priority=None, due=None):
    result = tasks
    if status == "pending":
        result = [t for t in result if not t.completed]
    elif status == "completed":
        result = [t for t in result if t.completed]
    if priority and priority != "all":
        result = [t for t in result if t.priority.value == priority]
    if due == "today":
        result = [t for t in result if t.due_date == date.today()]
    elif due == "week":
        result = [t for t in result if t.due_date and t.due_date <= date.today() + timedelta(days=7)]
    elif due == "overdue":
        result = [t for t in result if t.is_overdue]
    return result
```

**Acceptance Tests**:
- [ ] Search matches title (case-insensitive)
- [ ] Search matches description (case-insensitive)
- [ ] Empty search results show message
- [ ] Filter by status works
- [ ] Filter by priority works
- [ ] Filter by due date works
- [ ] Filters combine correctly
- [ ] Result count displayed

---

### Phase 4: Sort Tasks (Intermediate Level - Feature 3)

**Objective**: Enable custom task ordering

**CLI Commands**:
```bash
# Sort by due date
todo list --sort due_date

# Sort by priority
todo list --sort priority

# Sort alphabetically
todo list --sort title

# Reverse sort
todo list --sort priority --reverse

# Combined with filter
todo list --status pending --sort priority
```

**Implementation Steps**:
1. Add `--sort` argument with choices: due_date, priority, title, created
2. Add `--reverse` flag
3. Implement sort functions with null handling
4. Ensure stable sort for equal values

**Sort Logic**:
```python
def sort_tasks(tasks, sort_by="created", reverse=False):
    if sort_by == "due_date":
        sentinel = date.max if not reverse else date.min
        return sorted(tasks, key=lambda t: t.due_date or sentinel, reverse=reverse)
    elif sort_by == "priority":
        return sorted(tasks, key=lambda t: t.priority.sort_key(), reverse=reverse)
    elif sort_by == "title":
        return sorted(tasks, key=lambda t: t.title.lower(), reverse=reverse)
    else:  # created
        return sorted(tasks, key=lambda t: t.created_at, reverse=reverse)
```

**Acceptance Tests**:
- [ ] Sort by due_date (nulls at end)
- [ ] Sort by priority (high first by default)
- [ ] Sort by title (A-Z, case-insensitive)
- [ ] Sort by created_at (default)
- [ ] Reverse flag works
- [ ] Sort combines with filters

---

### Phase 5: Due Dates & Time (Advanced Level - Feature 5 Part 1)

**Objective**: Enable deadline tracking

**CLI Commands**:
```bash
# Add with due date
todo add "Task" --due 2025-01-15

# Add with due date and time
todo add "Meeting" --due 2025-01-15 --time 14:30

# Update due date
todo update <id> --due 2025-01-20

# Remove due date
todo update <id> --due none
```

**Implementation Steps**:
1. Add `--due` argument (YYYY-MM-DD or "none")
2. Add `--time` argument (HH:MM)
3. Implement date/time parsing and validation
4. Reject past dates
5. Reject time without date
6. Update display format

**Validation**:
```python
def validate_due_date(date_str):
    if date_str == "none":
        return None
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
        if d < date.today():
            raise ValueError("Due date cannot be in the past")
        return d
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")

def validate_due_time(time_str, has_due_date):
    if time_str and not has_due_date:
        raise ValueError("Due time requires a due date")
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        raise ValueError("Invalid time format. Use HH:MM")
```

**Acceptance Tests**:
- [ ] Due date set in YYYY-MM-DD format
- [ ] Due time set in HH:MM format
- [ ] Past dates rejected
- [ ] Time without date rejected
- [ ] Due date updateable
- [ ] Due date removable with "none"
- [ ] Display format correct

---

### Phase 6: Reminders (Advanced Level - Feature 5 Part 2)

**Objective**: Visual indicators for upcoming/overdue tasks

**CLI Commands**:
```bash
# List shows reminder/overdue indicators
todo list

# View only tasks needing attention
todo reminders

# Configure threshold
todo config reminder-threshold 12h

# View configuration
todo config
```

**Implementation Steps**:
1. Add computed properties `is_overdue` and `is_reminder`
2. Update display format with `[OVERDUE]` and `[REMINDER]` prefixes
3. Add `reminders` subcommand
4. Add `config` subcommand with `reminder-threshold` setting
5. Implement threshold parsing (1h, 6h, 12h, 24h, 48h, 7d)

**Computed Properties**:
```python
@property
def is_overdue(self) -> bool:
    if self.completed or not self.due_date:
        return False
    due_datetime = self._get_due_datetime()
    return due_datetime < datetime.now()

@property
def is_reminder(self) -> bool:
    if self.completed or not self.due_date or self.is_overdue:
        return False
    due_datetime = self._get_due_datetime()
    threshold = config.reminder_threshold
    return datetime.now() <= due_datetime <= datetime.now() + threshold
```

**Acceptance Tests**:
- [ ] `[OVERDUE]` shown for past-due tasks
- [ ] `[REMINDER]` shown for tasks within threshold
- [ ] `reminders` command filters correctly
- [ ] Default threshold is 24h
- [ ] Threshold configurable
- [ ] `config` displays current settings

---

### Phase 7: Recurring Tasks (Advanced Level - Feature 4)

**Objective**: Auto-create next occurrence on completion

**CLI Commands**:
```bash
# Create recurring task
todo add "Standup" --due 2025-01-01 --recurrence daily

# Complete triggers new task creation
todo complete <id>

# Update recurrence
todo update <id> --recurrence weekly

# Remove recurrence
todo update <id> --recurrence none
```

**Implementation Steps**:
1. Add `--recurrence` argument (daily, weekly, monthly, none)
2. Require due_date for recurrence != none
3. Update display format with `(repeats: pattern)`
4. Implement recurrence calculation in `recurrence.py`
5. Hook into `complete` command to create next occurrence

**Recurrence Calculation**:
```python
def calculate_next_due_date(current_date: date, pattern: Recurrence) -> date:
    if pattern == Recurrence.DAILY:
        return current_date + timedelta(days=1)
    elif pattern == Recurrence.WEEKLY:
        return current_date + timedelta(days=7)
    elif pattern == Recurrence.MONTHLY:
        year = current_date.year + (current_date.month // 12)
        month = (current_date.month % 12) + 1
        max_day = monthrange(year, month)[1]
        day = min(current_date.day, max_day)
        return date(year, month, day)
    return current_date  # NONE case - shouldn't be called
```

**Complete Flow**:
```python
def complete_task(task_id: int) -> Tuple[Task, Optional[Task]]:
    task = store.get(task_id)
    task.completed = True
    task.updated_at = datetime.now()

    new_task = None
    if task.recurrence != Recurrence.NONE:
        new_task = Task(
            title=task.title,
            description=task.description,
            priority=task.priority,
            tags=task.tags.copy(),
            recurrence=task.recurrence,
            due_date=calculate_next_due_date(task.due_date, task.recurrence),
            due_time=task.due_time,
        )
        store.add(new_task)

    return task, new_task
```

**Acceptance Tests**:
- [ ] Daily recurrence: +1 day
- [ ] Weekly recurrence: +7 days
- [ ] Monthly recurrence: +1 month (with day clamping)
- [ ] Jan 31 → Feb 28 edge case
- [ ] New task has same title, description, priority, tags
- [ ] New task has new ID, pending status
- [ ] Recurrence requires due_date
- [ ] Recurrence updateable
- [ ] Recurrence removable

---

## CLI Command Summary

| Command | Description | New Flags |
|---------|-------------|-----------|
| `add` | Create task | `--priority`, `--tags`, `--due`, `--time`, `--recurrence` |
| `update` | Modify task | `--priority`, `--tags`, `--due`, `--time`, `--recurrence` |
| `list` | View tasks | `--status`, `--priority`, `--due`, `--sort`, `--reverse` |
| `search` | Find tasks | `<keyword>` (positional) |
| `complete` | Mark done | (triggers recurrence) |
| `reminders` | Due soon | (no args) |
| `config` | Settings | `reminder-threshold <value>` |

---

## Error Messages

| Scenario | Message |
|----------|---------|
| Invalid priority | "Invalid priority. Use: high, medium, low" |
| Invalid tag format | "Invalid tag format. Tags must be alphanumeric with hyphens/underscores, max 50 chars" |
| Too many tags | "Maximum 10 tags allowed" |
| Invalid date format | "Invalid date format. Use YYYY-MM-DD" |
| Past date | "Due date cannot be in the past" |
| Time without date | "Due time requires a due date. Use --due YYYY-MM-DD --time HH:MM" |
| Invalid time format | "Invalid time format. Use HH:MM (24-hour)" |
| Recurrence without date | "Recurring tasks must have a due date. Use --due YYYY-MM-DD" |
| Invalid threshold | "Invalid threshold format. Use: 1h, 6h, 12h, 24h, 48h, 7d" |
| No search results | "No tasks found matching 'keyword'" |
| No filter results | "No tasks match the specified filters" |

---

## Test Strategy

### Unit Tests (per module)
- `test_models.py`: Priority enum, Recurrence enum, Task validation, computed properties
- `test_task_store.py`: CRUD operations, ID generation
- `test_task_service.py`: Search, filter, sort, complete with recurrence
- `test_recurrence.py`: Date calculations, edge cases (month-end)
- `test_formatters.py`: Display strings, indicator prefixes

### Integration Tests
- `test_cli.py`: End-to-end command execution with all flag combinations

### Contract Tests
- `test_validation.py`: All input validation rules, error messages

### TDD Order
1. Write failing test for validation rule
2. Implement validation
3. Refactor if needed
4. Repeat for each functional requirement

---

## Dependencies (Implementation Order)

```
Phase 1: Core Models
    ↓
Phase 2: Priority & Tags (FR-P001-P005, FR-T001-T007)
    ↓
Phase 5: Due Dates (FR-D001-D007) ← Required by Phase 3 filters
    ↓
Phase 3: Search & Filter (FR-S001-S004, FR-F001-F006)
    ↓
Phase 4: Sort (FR-SO001-SO007)
    ↓
Phase 6: Reminders (FR-REM001-REM008)
    ↓
Phase 7: Recurring Tasks (FR-R001-R012) ← Depends on due dates
```

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Monthly recurrence edge cases | Medium | Medium | Comprehensive unit tests for all month-end scenarios |
| Filter/sort performance at scale | Low | Low | Simple list operations; profile if >1s |
| CLI argument conflicts | Low | Medium | Careful argparse design; integration tests |

---

## Ready for /sp.tasks

This plan is ready for task generation. Execute `/sp.tasks` to generate the implementation task list.

**Checklist**:
- [x] All 5 features have implementation phases
- [x] All 47 functional requirements mapped to phases
- [x] Test strategy defined
- [x] Dependencies identified
- [x] Error messages specified
- [x] CLI commands documented
