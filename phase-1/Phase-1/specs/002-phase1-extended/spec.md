# Feature Specification: Phase 1 Extended Features

**Feature Branch**: `002-phase1-extended`
**Created**: 2025-12-29
**Status**: Draft
**Input**: User description: "Phase 1 Extended Features - Add Intermediate Level (Priorities, Tags, Search, Filter, Sort) and Advanced Level (Recurring Tasks, Due Dates & Reminders) to the In-Memory Python Console App"

---

## Overview

This specification extends the Phase 1 Todo Console Application beyond Basic Level (Add, Delete, Update, View, Mark Complete) to include:

- **Intermediate Level**: Organization & Usability features
- **Advanced Level**: Intelligent automation features

All features maintain Phase 1 constraints: Python, in-memory storage, CLI interface only.

---

## PART A: Intermediate Level (Organization & Usability)

---

### Feature 1: Priorities & Tags/Categories

#### Problem Statement

Users need to organize tasks by importance and context. Without priority levels, users cannot quickly identify which tasks need immediate attention. Without tags/categories, users cannot group related tasks or filter by context (work vs home).

#### User Scenarios & Testing

##### User Story 1.1 - Assign Priority to Task (Priority: P1)

As a user, I want to assign a priority level (high, medium, low) to my tasks so I can focus on what's most important.

**Why this priority**: Core organizational feature - enables users to identify urgent work immediately.

**Independent Test**: Can be fully tested by creating a task with `--priority high` and verifying it displays the priority indicator.

**Acceptance Scenarios**:

1. **Given** user is adding a new task, **When** user specifies `--priority high`, **Then** task is created with high priority and displays `[HIGH]` indicator
2. **Given** user is adding a task without priority, **When** task is created, **Then** task defaults to medium priority
3. **Given** user has an existing task, **When** user updates with `--priority low`, **Then** task priority changes to low

---

##### User Story 1.2 - Categorize Tasks with Tags (Priority: P1)

As a user, I want to add tags/categories to my tasks so I can organize them by context.

**Why this priority**: Essential for task organization - allows grouping by work, home, personal, etc.

**Independent Test**: Can be fully tested by creating a task with `--tags work,urgent` and verifying tags display correctly.

**Acceptance Scenarios**:

1. **Given** user is adding a new task, **When** user specifies `--tags work,urgent`, **Then** task is created with both tags attached
2. **Given** user has a task with tags, **When** user updates tags to `--tags home`, **Then** previous tags are replaced with new tags
3. **Given** user creates task without tags, **When** task is displayed, **Then** no tag indicator appears

---

#### Functional Requirements

- **FR-P001**: System MUST support exactly three priority levels: `high`, `medium`, `low`
- **FR-P002**: Each task MUST have exactly one priority (default: `medium`)
- **FR-P003**: System MUST display priority indicator in task list view using format `[HIGH]`, `[MEDIUM]`, `[LOW]`
- **FR-P004**: System MUST allow priority to be set at task creation via `--priority` flag
- **FR-P005**: System MUST allow priority to be updated via `update <id> --priority <level>`
- **FR-T001**: System MUST support user-defined tags as comma-separated strings
- **FR-T002**: Each task MAY have zero or more tags
- **FR-T003**: System MUST display tags in task list using format `[tags: tag1, tag2]`
- **FR-T004**: System MUST allow tags to be set at task creation via `--tags` flag
- **FR-T005**: System MUST allow tags to be updated (replaced) via `update <id> --tags <tags>`
- **FR-T006**: Tag names MUST be case-insensitive and stored in lowercase
- **FR-T007**: System MUST reject empty tag names and tags containing only whitespace

#### Data Model Additions

| Field    | Type                       | Required | Default  | Description                   |
|----------|----------------------------|----------|----------|-------------------------------|
| priority | enum(high, medium, low)    | Yes      | medium   | Task importance level         |
| tags     | list[str]                  | No       | []       | Zero or more category labels  |

#### CLI Interaction Examples

```
# Add task with priority and tags
> add "Finish report" --priority high --tags work,deadline
Task 1 created: [HIGH] Finish report [tags: work, deadline]

# Add task with only priority
> add "Buy groceries" --priority low
Task 2 created: [LOW] Buy groceries

# Update priority
> update 2 --priority medium
Task 2 updated: [MEDIUM] Buy groceries

# Update tags
> update 1 --tags work,urgent,q4
Task 1 updated: [HIGH] Finish report [tags: work, urgent, q4]

# List all tasks
> list
1. [HIGH] [ ] Finish report [tags: work, urgent, q4]
2. [MEDIUM] [ ] Buy groceries
```

#### Acceptance Criteria

- [ ] Priority can be set to high, medium, or low
- [ ] Tasks default to medium priority when not specified
- [ ] Multiple tags can be assigned to a single task
- [ ] Tags are displayed in task list view
- [ ] Priority and tags can be updated independently
- [ ] Invalid priority values display helpful error message

---

### Feature 2: Search & Filter

#### Problem Statement

As the task list grows, users need efficient ways to find specific tasks. Without search, users must scroll through all tasks. Without filters, users cannot focus on specific subsets (e.g., only pending high-priority work tasks).

#### User Scenarios & Testing

##### User Story 2.1 - Search Tasks by Keyword (Priority: P1)

As a user, I want to search tasks by keyword so I can quickly find specific items.

**Why this priority**: Essential for large task lists - enables quick task location.

**Independent Test**: Can be fully tested by creating several tasks and searching with `search "keyword"`.

**Acceptance Scenarios**:

1. **Given** multiple tasks exist, **When** user searches for "report", **Then** all tasks containing "report" in title OR description are displayed
2. **Given** user searches for "xyz", **When** no tasks match, **Then** message "No tasks found matching 'xyz'" is displayed
3. **Given** tasks with "Report" and "REPORT", **When** user searches "report", **Then** both tasks are found (case-insensitive)

---

##### User Story 2.2 - Filter by Completion Status (Priority: P1)

As a user, I want to filter tasks by completion status so I can see only pending or completed work.

**Why this priority**: Critical for focus - users need to see what's left to do.

**Independent Test**: Can be fully tested by creating tasks, completing some, then filtering with `list --status pending`.

**Acceptance Scenarios**:

1. **Given** mix of completed and pending tasks, **When** user runs `list --status pending`, **Then** only incomplete tasks are shown
2. **Given** mix of completed and pending tasks, **When** user runs `list --status completed`, **Then** only completed tasks are shown
3. **Given** user runs `list --status all`, **When** tasks exist, **Then** all tasks are displayed regardless of status

---

##### User Story 2.3 - Filter by Priority (Priority: P2)

As a user, I want to filter tasks by priority so I can focus on high-priority items.

**Why this priority**: Enables focused work sessions on urgent items.

**Independent Test**: Can be fully tested by creating tasks with different priorities and filtering with `list --priority high`.

**Acceptance Scenarios**:

1. **Given** tasks with different priorities, **When** user runs `list --priority high`, **Then** only high-priority tasks are shown
2. **Given** user combines filters `list --status pending --priority high`, **When** executed, **Then** only pending high-priority tasks shown

---

##### User Story 2.4 - Filter by Due Date (Priority: P3)

As a user, I want to filter tasks by due date so I can see what's due soon.

**Why this priority**: Depends on due date feature; useful for deadline management.

**Independent Test**: Can be fully tested by creating tasks with due dates and filtering with `list --due today`.

**Acceptance Scenarios**:

1. **Given** tasks with various due dates, **When** user runs `list --due today`, **Then** only tasks due today are shown
2. **Given** user runs `list --due week`, **When** tasks exist, **Then** tasks due within next 7 days are shown
3. **Given** user runs `list --due overdue`, **When** overdue tasks exist, **Then** only past-due tasks are shown

---

#### Functional Requirements

- **FR-S001**: System MUST search against task title AND description fields
- **FR-S002**: Search MUST be case-insensitive
- **FR-S003**: Search MUST support partial matches (substring search)
- **FR-S004**: System MUST display count of matching results
- **FR-F001**: Filter by status MUST support values: `all`, `pending`, `completed`
- **FR-F002**: Filter by priority MUST support values: `all`, `high`, `medium`, `low`
- **FR-F003**: Filter by due date MUST support values: `all`, `today`, `week`, `overdue`
- **FR-F004**: Multiple filters MUST be combinable in single command
- **FR-F005**: Empty filter results MUST display message "No tasks match the specified filters"
- **FR-F006**: Default filter values MUST be `all` for status, priority, and due date

#### CLI Interaction Examples

```
# Search by keyword
> search "report"
Found 2 tasks matching 'report':
1. [HIGH] [ ] Finish quarterly report [tags: work]
3. [MEDIUM] [x] Review report template [tags: work]

# Filter by status
> list --status pending
Pending tasks (3):
1. [HIGH] [ ] Finish quarterly report
2. [LOW] [ ] Buy groceries
4. [MEDIUM] [ ] Call dentist

# Filter by priority
> list --priority high
High priority tasks (1):
1. [HIGH] [ ] Finish quarterly report

# Combined filters
> list --status pending --priority high
Pending high-priority tasks (1):
1. [HIGH] [ ] Finish quarterly report

# Filter by due date
> list --due today
Tasks due today (2):
1. [HIGH] [ ] Finish quarterly report [due: 2025-12-29]
4. [MEDIUM] [ ] Call dentist [due: 2025-12-29]
```

#### Acceptance Criteria

- [ ] Search matches both title and description (case-insensitive)
- [ ] Filter by status shows correct subset of tasks
- [ ] Filter by priority shows correct subset of tasks
- [ ] Multiple filters can be combined
- [ ] Empty results display appropriate message
- [ ] Result count is displayed with filtered results

---

### Feature 3: Sort Tasks

#### Problem Statement

Users need to view tasks in different orders based on their current focus. Default chronological order may not be optimal when planning work by deadline or importance.

#### User Scenarios & Testing

##### User Story 3.1 - Sort by Due Date (Priority: P2)

As a user, I want to sort tasks by due date so I can see upcoming deadlines first.

**Why this priority**: Essential for deadline management.

**Independent Test**: Can be fully tested by creating tasks with different due dates and sorting with `list --sort due_date`.

**Acceptance Scenarios**:

1. **Given** tasks with various due dates, **When** user runs `list --sort due_date`, **Then** tasks are ordered earliest due date first
2. **Given** tasks with due dates and some without, **When** sorted by due date, **Then** tasks without due dates appear at the end
3. **Given** user runs `list --sort due_date --reverse`, **When** executed, **Then** tasks ordered latest due date first

---

##### User Story 3.2 - Sort by Priority (Priority: P2)

As a user, I want to sort tasks by priority so I can see important items at the top.

**Why this priority**: Enables priority-based work planning.

**Independent Test**: Can be fully tested by creating tasks with different priorities and sorting with `list --sort priority`.

**Acceptance Scenarios**:

1. **Given** tasks with different priorities, **When** user runs `list --sort priority`, **Then** tasks ordered high -> medium -> low
2. **Given** user runs `list --sort priority --reverse`, **When** executed, **Then** tasks ordered low -> medium -> high

---

##### User Story 3.3 - Sort Alphabetically (Priority: P3)

As a user, I want to sort tasks alphabetically so I can find tasks by name.

**Why this priority**: Useful for locating specific tasks in large lists.

**Independent Test**: Can be fully tested by creating multiple tasks and sorting with `list --sort title`.

**Acceptance Scenarios**:

1. **Given** multiple tasks, **When** user runs `list --sort title`, **Then** tasks ordered A-Z by title
2. **Given** user runs `list --sort title --reverse`, **When** executed, **Then** tasks ordered Z-A

---

#### Functional Requirements

- **FR-SO001**: System MUST support sorting by: `due_date`, `priority`, `title`, `created` (default)
- **FR-SO002**: Default sort order MUST be by creation date (newest first)
- **FR-SO003**: Sort MUST be reversible via `--reverse` flag
- **FR-SO004**: Sort MUST work in combination with filters
- **FR-SO005**: Priority sort order MUST be: high (1) -> medium (2) -> low (3)
- **FR-SO006**: Tasks without due dates MUST appear after tasks with due dates when sorting by due_date
- **FR-SO007**: Alphabetical sort MUST be case-insensitive

#### CLI Interaction Examples

```
# Sort by due date (earliest first)
> list --sort due_date
1. [HIGH] [ ] Finish report [due: 2025-12-29]
2. [MEDIUM] [ ] Team meeting [due: 2025-12-30]
3. [LOW] [ ] Buy groceries [due: 2025-12-31]
4. [MEDIUM] [ ] Read book [no due date]

# Sort by priority (high first)
> list --sort priority
1. [HIGH] [ ] Finish report
2. [MEDIUM] [ ] Team meeting
3. [MEDIUM] [ ] Read book
4. [LOW] [ ] Buy groceries

# Sort alphabetically (A-Z)
> list --sort title
1. [LOW] [ ] Buy groceries
2. [HIGH] [ ] Finish report
3. [MEDIUM] [ ] Read book
4. [MEDIUM] [ ] Team meeting

# Reverse sort
> list --sort title --reverse
4. [MEDIUM] [ ] Team meeting
3. [MEDIUM] [ ] Read book
2. [HIGH] [ ] Finish report
1. [LOW] [ ] Buy groceries

# Combined with filter
> list --status pending --sort priority
```

#### Acceptance Criteria

- [ ] Tasks can be sorted by due date, priority, title, or creation date
- [ ] Default sort is by creation date (newest first)
- [ ] Sort order can be reversed with `--reverse` flag
- [ ] Sort works correctly with filters
- [ ] Tasks without due dates appear at end when sorting by due_date

---

## PART B: Advanced Level (Intelligent Features)

---

### Feature 4: Recurring Tasks

#### Problem Statement

Many tasks repeat on a regular schedule (daily standup, weekly review, monthly reports). Users currently must manually recreate these tasks each time, which is tedious and error-prone.

#### User Scenarios & Testing

##### User Story 4.1 - Create Daily Recurring Task (Priority: P1)

As a user, I want to create tasks that repeat daily so I can track routine activities without manual recreation.

**Why this priority**: Core recurrence functionality.

**Independent Test**: Can be fully tested by creating a daily recurring task, completing it, and verifying the next occurrence is created.

**Acceptance Scenarios**:

1. **Given** user creates task with `--recurrence daily --due 2025-01-01`, **When** task is created, **Then** task shows `(repeats: daily)` indicator
2. **Given** daily recurring task is marked complete, **When** completion occurs, **Then** new task is created with due date = original + 1 day
3. **Given** new recurring task is created, **When** displayed, **Then** it has same title, description, priority, and tags as original

---

##### User Story 4.2 - Create Weekly Recurring Task (Priority: P1)

As a user, I want to create tasks that repeat weekly so I can manage weekly commitments.

**Why this priority**: Common recurrence pattern for meetings, reviews.

**Independent Test**: Can be fully tested by creating weekly task, completing it, verifying next occurrence is 7 days later.

**Acceptance Scenarios**:

1. **Given** user creates task with `--recurrence weekly --due 2025-01-01`, **When** task is completed, **Then** new task created with due date = original + 7 days
2. **Given** weekly task completed on 2025-01-01 (Wednesday), **When** next task created, **Then** due date is 2025-01-08 (Wednesday)

---

##### User Story 4.3 - Create Monthly Recurring Task (Priority: P2)

As a user, I want to create tasks that repeat monthly so I can handle monthly responsibilities.

**Why this priority**: Less common but important for bills, reports.

**Independent Test**: Can be fully tested by creating monthly task, completing it, verifying next occurrence is 1 month later.

**Acceptance Scenarios**:

1. **Given** user creates task with `--recurrence monthly --due 2025-01-15`, **When** task is completed, **Then** new task created with due date = 2025-02-15
2. **Given** monthly task due on Jan 31, **When** completed, **Then** next due date is Feb 28 (or 29 in leap year)
3. **Given** monthly task due on Jan 30, **When** February has 28 days, **Then** next due date is Feb 28

---

##### User Story 4.4 - Modify or Remove Recurrence (Priority: P2)

As a user, I want to change or remove recurrence from a task so I can adjust my schedule.

**Why this priority**: Flexibility for changing needs.

**Independent Test**: Can be fully tested by updating recurrence pattern or removing it entirely.

**Acceptance Scenarios**:

1. **Given** daily recurring task exists, **When** user updates with `--recurrence weekly`, **Then** task now repeats weekly
2. **Given** recurring task exists, **When** user updates with `--recurrence none`, **Then** task becomes one-time task
3. **Given** one-time task exists, **When** user adds `--recurrence daily`, **Then** task becomes recurring

---

#### Functional Requirements

- **FR-R001**: System MUST support recurrence patterns: `daily`, `weekly`, `monthly`, `none`
- **FR-R002**: Recurrence MUST be optional (default: `none` / one-time task)
- **FR-R003**: Recurring tasks MUST have a due date set
- **FR-R004**: When recurring task is completed, system MUST automatically create new task
- **FR-R005**: New recurring task MUST copy: title, description, priority, tags, recurrence pattern
- **FR-R006**: New recurring task MUST have: new ID, status=pending, calculated due date
- **FR-R007**: Daily recurrence: next due_date = current due_date + 1 day
- **FR-R008**: Weekly recurrence: next due_date = current due_date + 7 days
- **FR-R009**: Monthly recurrence: next due_date = current due_date + 1 month (same day, or last day if overflow)
- **FR-R010**: Recurrence MUST be displayed in task list as `(repeats: pattern)`
- **FR-R011**: Recurrence MUST be editable via `update <id> --recurrence <pattern>`
- **FR-R012**: Attempting to set recurrence without due date MUST display error message

#### Data Model Additions

| Field      | Type                                  | Required | Default | Description        |
|------------|---------------------------------------|----------|---------|--------------------|
| recurrence | enum(daily, weekly, monthly, none)    | No       | none    | Recurrence pattern |

#### CLI Interaction Examples

```
# Create daily recurring task
> add "Morning standup" --due 2025-01-01 --recurrence daily --priority high --tags work
Task 1 created: [HIGH] Morning standup (repeats: daily) [due: 2025-01-01] [tags: work]

# Create weekly recurring task
> add "Weekly review" --due 2025-01-06 --recurrence weekly
Task 2 created: [MEDIUM] Weekly review (repeats: weekly) [due: 2025-01-06]

# Complete recurring task - triggers auto-creation
> complete 1
Task 1 completed: [HIGH] Morning standup
New recurring task created:
Task 3: [HIGH] Morning standup (repeats: daily) [due: 2025-01-02] [tags: work]

# Update recurrence pattern
> update 2 --recurrence monthly
Task 2 updated: [MEDIUM] Weekly review (repeats: monthly) [due: 2025-01-06]

# Remove recurrence
> update 2 --recurrence none
Task 2 updated: [MEDIUM] Weekly review [due: 2025-01-06]

# Error: recurrence without due date
> add "Bad task" --recurrence daily
Error: Recurring tasks must have a due date. Use --due YYYY-MM-DD
```

#### Acceptance Criteria

- [ ] Tasks can be created with daily, weekly, or monthly recurrence
- [ ] Completing a recurring task automatically creates the next occurrence
- [ ] New occurrence has correct calculated due date
- [ ] New occurrence preserves title, description, priority, tags
- [ ] Recurrence can be modified or removed
- [ ] Error displayed if recurrence set without due date

#### Phase 1 Constraints

- Recurrence triggered ONLY when user marks task complete (synchronous)
- No background scheduling or cron jobs
- All logic executes during the `complete` command

---

### Feature 5: Due Dates & Time Reminders

#### Problem Statement

Users need to track deadlines and be reminded of upcoming tasks. Without due dates, users cannot manage time-sensitive work. Without reminders, users may miss deadlines.

#### User Scenarios & Testing

##### User Story 5.1 - Set Due Date on Task (Priority: P1)

As a user, I want to set a due date for my tasks so I can track deadlines.

**Why this priority**: Core deadline tracking functionality.

**Independent Test**: Can be fully tested by creating task with `--due 2025-01-15` and verifying display.

**Acceptance Scenarios**:

1. **Given** user creates task with `--due 2025-01-15`, **When** task is created, **Then** task displays `[due: 2025-01-15]`
2. **Given** user updates task with `--due 2025-01-20`, **When** update completes, **Then** due date changes to new value
3. **Given** user tries to set past date `--due 2020-01-01`, **When** command executed, **Then** error message displayed

---

##### User Story 5.2 - Set Due Time on Task (Priority: P2)

As a user, I want to set a specific time for my due date so I can be precise about deadlines.

**Why this priority**: Enhances deadline precision for time-sensitive tasks.

**Independent Test**: Can be fully tested by creating task with `--due 2025-01-15 --time 14:30`.

**Acceptance Scenarios**:

1. **Given** user creates task with `--due 2025-01-15 --time 14:30`, **When** task created, **Then** displays `[due: 2025-01-15 14:30]`
2. **Given** user sets time without date `--time 14:30`, **When** command executed, **Then** error message displayed
3. **Given** invalid time format `--time 25:99`, **When** command executed, **Then** error with valid format hint

---

##### User Story 5.3 - View Reminders for Due Tasks (Priority: P1)

As a user, I want to see reminders for tasks that are due soon so I don't miss deadlines.

**Why this priority**: Critical for deadline awareness.

**Independent Test**: Can be fully tested by creating tasks due within 24 hours and running `reminders` command.

**Acceptance Scenarios**:

1. **Given** task due within 24 hours, **When** user runs `list`, **Then** task shows `[REMINDER]` prefix
2. **Given** task past due date, **When** user runs `list`, **Then** task shows `[OVERDUE]` prefix
3. **Given** user runs `reminders`, **When** tasks due soon exist, **Then** only those tasks are displayed

---

##### User Story 5.4 - Configure Reminder Threshold (Priority: P3)

As a user, I want to configure the reminder threshold so I can customize when I'm reminded.

**Why this priority**: Nice-to-have customization.

**Independent Test**: Can be fully tested by setting threshold with `config reminder-threshold 12h`.

**Acceptance Scenarios**:

1. **Given** default threshold is 24h, **When** user runs `config reminder-threshold 12h`, **Then** threshold changes to 12 hours
2. **Given** threshold is 12h and task due in 10 hours, **When** user runs `list`, **Then** task shows `[REMINDER]`
3. **Given** threshold is 12h and task due in 15 hours, **When** user runs `list`, **Then** no reminder indicator shown

---

#### Functional Requirements

- **FR-D001**: System MUST accept due date in ISO format (YYYY-MM-DD)
- **FR-D002**: System MUST accept optional due time in 24-hour format (HH:MM)
- **FR-D003**: System MUST reject due dates in the past with error message
- **FR-D004**: System MUST reject due time without due date
- **FR-D005**: System MUST display due date/time in task list as `[due: YYYY-MM-DD HH:MM]`
- **FR-D006**: Due date/time MUST be editable via `update <id> --due <date> [--time <time>]`
- **FR-D007**: Due date MUST be removable via `update <id> --due none`
- **FR-REM001**: System MUST identify tasks due within reminder threshold as "reminder" tasks
- **FR-REM002**: System MUST identify tasks past due date as "overdue" tasks
- **FR-REM003**: System MUST display `[REMINDER]` prefix for tasks due within threshold
- **FR-REM004**: System MUST display `[OVERDUE]` prefix for past-due tasks
- **FR-REM005**: Default reminder threshold MUST be 24 hours
- **FR-REM006**: Reminder threshold MUST be configurable via `config reminder-threshold <value>`
- **FR-REM007**: Supported threshold formats: `1h`, `6h`, `12h`, `24h`, `48h`, `7d`
- **FR-REM008**: `reminders` command MUST display only tasks due within threshold or overdue

#### Data Model Additions

| Field    | Type              | Required | Default | Description                              |
|----------|-------------------|----------|---------|------------------------------------------|
| due_date | date (YYYY-MM-DD) | No       | null    | Task deadline date                       |
| due_time | time (HH:MM)      | No       | null    | Task deadline time (requires due_date)   |

#### Configuration

| Setting            | Type     | Default | Description                              |
|--------------------|----------|---------|------------------------------------------|
| reminder_threshold | duration | 24h     | Time before due date to show reminder    |

#### CLI Interaction Examples

```
# Add task with due date
> add "Submit report" --due 2025-01-15
Task 1 created: [MEDIUM] Submit report [due: 2025-01-15]

# Add task with due date and time
> add "Team meeting" --due 2025-01-15 --time 14:30 --priority high
Task 2 created: [HIGH] Team meeting [due: 2025-01-15 14:30]

# Update due date
> update 1 --due 2025-01-20
Task 1 updated: [MEDIUM] Submit report [due: 2025-01-20]

# Remove due date
> update 1 --due none
Task 1 updated: [MEDIUM] Submit report

# Error: past date
> add "Old task" --due 2020-01-01
Error: Due date cannot be in the past. Please use a future date.

# Error: time without date
> add "Bad task" --time 14:30
Error: Due time requires a due date. Use --due YYYY-MM-DD --time HH:MM

# List with reminder and overdue indicators
> list
1. [OVERDUE] [HIGH] [ ] Submit proposal [due: 2025-12-28]
2. [REMINDER] [MEDIUM] [ ] Team meeting [due: 2025-12-29 14:30]
3. [LOW] [ ] Buy groceries [due: 2025-12-31]

# View only reminder/overdue tasks
> reminders
Tasks requiring attention (2):
1. [OVERDUE] [HIGH] [ ] Submit proposal [due: 2025-12-28]
2. [REMINDER] [MEDIUM] [ ] Team meeting [due: 2025-12-29 14:30]

# Configure reminder threshold
> config reminder-threshold 12h
Reminder threshold set to 12 hours

# View current configuration
> config
Current settings:
- reminder_threshold: 12h
```

#### Validation Rules

- Due date MUST be today or in the future (at time of setting)
- Due time requires due date to be set
- Time format MUST be HH:MM (24-hour, 00:00 to 23:59)
- Date format MUST be YYYY-MM-DD
- Invalid formats display helpful error with correct format example

#### Acceptance Criteria

- [ ] Tasks can have due date set in YYYY-MM-DD format
- [ ] Tasks can have optional due time in HH:MM format
- [ ] Past dates are rejected with error message
- [ ] Due time without date is rejected with error message
- [ ] Tasks due within threshold show [REMINDER] indicator
- [ ] Past-due tasks show [OVERDUE] indicator
- [ ] Reminder threshold is configurable
- [ ] `reminders` command shows only relevant tasks

#### Phase 1 Constraints

- No push notifications or system alerts (console output only)
- No background workers or scheduled checks
- Reminders checked on-demand when running `list` or `reminders`
- All date/time validation at input time only

---

## Edge Cases (All Features)

### Priorities & Tags
- Empty tag string `--tags ""` should be treated as no tags
- Tag with special characters should be sanitized or rejected
- Very long tag names should be truncated or rejected (max 50 chars)
- Duplicate tags in list should be deduplicated

### Search & Filter
- Search for empty string should return all tasks or error
- Search with only whitespace should be treated as empty
- Filter combination with no matches should show helpful message
- Case sensitivity edge cases (Turkish I, German ß)

### Sort
- Sorting empty task list should display "No tasks to display"
- Tasks with identical sort values should maintain stable order
- Null values (no due date) consistently appear at end

### Recurring Tasks
- Monthly recurrence from Jan 31 to February (28 or 29 days)
- Monthly recurrence from March 31 to April (30 days)
- Completing task multiple times rapidly should not create duplicates
- Deleting recurring task should not create new occurrence

### Due Dates & Reminders
- Timezone handling (use system local time)
- Midnight edge case (23:59 vs 00:00)
- Leap year February 29
- Task due "today" at time already passed
- Config with invalid threshold format

---

## Key Entities Summary

### Task (Extended)

| Attribute   | Type     | Description                                  |
|-------------|----------|----------------------------------------------|
| id          | integer  | Unique identifier (auto-generated)           |
| title       | string   | Task title (required, 1-200 chars)           |
| description | string   | Task description (optional, max 1000 chars)  |
| completed   | boolean  | Completion status (default: false)           |
| priority    | enum     | high, medium, low (default: medium)          |
| tags        | list[str]| Zero or more category labels                 |
| due_date    | date     | Deadline date YYYY-MM-DD (optional)          |
| due_time    | time     | Deadline time HH:MM (optional)               |
| recurrence  | enum     | daily, weekly, monthly, none (default: none) |
| created_at  | datetime | Creation timestamp                           |
| updated_at  | datetime | Last modification timestamp                  |

### Configuration

| Setting            | Type     | Default | Description                            |
|--------------------|----------|---------|----------------------------------------|
| reminder_threshold | duration | 24h     | Time window for showing reminders      |

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can organize tasks with priority and tags within 5 seconds per task
- **SC-002**: Users can find specific tasks via search in under 2 seconds
- **SC-003**: Users can view filtered/sorted task lists with single command
- **SC-004**: 100% of recurring task completions generate correct next occurrence
- **SC-005**: Users receive visual indicators for all tasks due within configured threshold
- **SC-006**: Zero past-date tasks can be created (validation prevents 100%)
- **SC-007**: All commands complete within 1 second for lists up to 1000 tasks

---

## Assumptions

1. **Single User**: Application serves one user (no multi-user support in Phase 1)
2. **Local Time**: All dates/times use system local timezone
3. **Session Persistence**: In-memory storage means data lost on application exit
4. **ASCII Tags**: Tag names support alphanumeric characters, hyphens, underscores
5. **English Interface**: All messages and prompts in English
6. **Sequential IDs**: Task IDs are auto-incrementing integers starting from 1
7. **Immediate Recurrence**: New recurring task created immediately upon completion (not scheduled)

---

## Out of Scope (Phase 1)

- Database persistence
- Multi-user support
- Web or GUI interface
- Push notifications
- Background task scheduling
- Task dependencies
- Subtasks
- File attachments
- Export/import functionality
- Undo/redo operations
