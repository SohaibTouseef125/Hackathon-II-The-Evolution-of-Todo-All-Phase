<!--
Sync Impact Report
==================
Version change: 1.0.0 → 1.1.0 (MINOR - new sections added)
Modified principles: None (existing principles preserved)
Added sections:
  - VII. Intermediate Level Features (Organization & Usability)
  - VIII. Advanced Level Features (Intelligent Features)
Removed sections: None
Templates requiring updates:
  - specs/<feature>/spec.md: ✅ No update needed (additive change)
  - specs/<feature>/plan.md: ✅ No update needed (additive change)
  - specs/<feature>/tasks.md: ✅ No update needed (additive change)
Follow-up TODOs: NoneJ
-->

# Todo App Phase I Constitution
<!-- Constitution for Hackathon II Todo App Phase I: In-Memory Python Console App -->

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All code must be generated through specification refinement using Claude Code and Spec-Kit Plus; No manual coding is allowed; Code generation must come from Claude Code based on well-defined and refined specifications; Specs must be complete and clear before implementation begins.

### II. Python Console Application Focus
Implementation must be a command-line interface application with in-memory storage; Must implement all 5 Basic Level features: Add Task, Delete Task, Update Task, View Task List, Mark as Complete; Application must be executable from the command line with clear user prompts and responses.

### III. Test-First Approach (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced; All functionality must have corresponding unit tests; Console interface must be testable with input/output verification.

### IV. Clean Code and Python Best Practices
Follow proper Python project structure with clear module organization; Adhere to PEP 8 style guidelines; Use meaningful variable and function names; Include appropriate docstrings and comments; Follow Python naming conventions and idioms.

### V. Technology Stack Compliance
Must use UV for package management; Must use Python 3.13+; Claude Code must be the primary implementation tool; Spec-Kit Plus must be used for specification management; No deviation from specified technology stack without explicit approval.

### VI. Functional Completeness

All Basic Level Todo features must be implemented: Add Task (create new todo items), Delete Task (remove tasks from the list), Update Task (modify existing task details), View Task List (display all tasks with status indicators), Mark as Complete (toggle task completion status).

---

## Feature Levels

### Basic Level (Core Essentials)

The foundational features required for the Phase I MVP:

1. **Add Task** - Create new todo items with title and optional description
2. **Delete Task** - Remove tasks from the list by ID
3. **Update Task** - Modify existing task details (title, description)
4. **View Task List** - Display all tasks with status indicators
5. **Mark as Complete** - Toggle task completion status

---

### VII. Intermediate Level (Organization & Usability)

These features enhance the application with organization and usability improvements while maintaining the in-memory, console-based constraints of Phase I.

#### 1. Priorities & Tags/Categories

##### User Stories
- As a user, I want to assign a priority level to my tasks so I can focus on what's most important
- As a user, I want to categorize my tasks with tags so I can organize them by context
- As a user, I want to view tasks by priority or tag so I can filter my work

##### Acceptance Criteria
- Priority levels MUST be one of: `high`, `medium`, `low`
- Each task MUST have exactly one priority (default: `medium`)
- Tags/categories MUST support values like: `work`, `home`, `personal`, `shopping`, `health`, etc.
- Each task MAY have zero or more tags (multiple tags per task allowed)
- Priority and tags MUST be displayed in task list view
- Priority and tags MUST be editable via update task functionality

##### Required Data Fields
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| priority | enum | Yes | "medium" | One of: high, medium, low |
| tags | list[str] | No | [] | Zero or more category labels |

##### Console (CLI) Behavior
- Add task: `add "Task title" --priority high --tags work,urgent`
- Update priority: `update <id> --priority low`
- Add/remove tags: `update <id> --tags home,personal`
- Display format: `[ID] [PRIORITY] [STATUS] Title [tags: work, urgent]`

---

#### 2. Search & Filter

##### User Stories
- As a user, I want to search tasks by keyword so I can quickly find specific items
- As a user, I want to filter tasks by completion status so I can see pending or completed work
- As a user, I want to filter tasks by priority so I can focus on high-priority items
- As a user, I want to filter tasks by date so I can see tasks due within a timeframe

##### Acceptance Criteria
- Search MUST match against task title AND description (case-insensitive)
- Filter by status MUST support: `all`, `pending`, `completed`
- Filter by priority MUST support: `all`, `high`, `medium`, `low`
- Filter by date MUST support filtering by due date (when due dates are implemented)
- Multiple filters MAY be combined (e.g., pending + high priority)
- Empty search/filter results MUST display appropriate message

##### Required Data Fields
No additional fields required (uses existing task fields)

##### Console (CLI) Behavior
- Search: `search "keyword"`
- Filter by status: `list --status pending`
- Filter by priority: `list --priority high`
- Combined filters: `list --status pending --priority high`
- Display: Shows filtered results with match count

---

#### 3. Sort Tasks

##### User Stories
- As a user, I want to sort tasks by due date so I can see upcoming deadlines first
- As a user, I want to sort tasks by priority so I can see important items at the top
- As a user, I want to sort tasks alphabetically so I can find tasks by name

##### Acceptance Criteria
- Sort by due date MUST order tasks by due_date field (earliest first by default)
- Sort by priority MUST order: high → medium → low (or reverse)
- Sort alphabetically MUST order by title (A-Z or Z-A)
- Sort order MUST be reversible (ascending/descending)
- Default sort order MUST be by creation date (newest first)
- Sort MUST work in combination with filters

##### Required Data Fields
No additional fields required (uses existing task fields)

##### Console (CLI) Behavior
- Sort by due date: `list --sort due_date`
- Sort by priority: `list --sort priority`
- Sort alphabetically: `list --sort title`
- Reverse order: `list --sort title --reverse`
- Combined: `list --status pending --sort priority`

---

### VIII. Advanced Level (Intelligent Features)

These features add intelligence and automation to the application while respecting Phase I constraints (in-memory only, no background workers, no async scheduling).

#### 1. Recurring Tasks

##### User Stories
- As a user, I want to create tasks that repeat daily so I can track routine activities
- As a user, I want to create tasks that repeat weekly so I can manage weekly commitments
- As a user, I want to create tasks that repeat monthly so I can handle monthly responsibilities
- As a user, I want the next occurrence to be created automatically when I complete a recurring task

##### Acceptance Criteria
- Recurrence patterns MUST support: `daily`, `weekly`, `monthly`
- Recurrence MUST be optional (tasks can be one-time or recurring)
- When a recurring task is marked complete:
  - The current task MUST be marked as completed
  - A new task MUST be automatically created with:
    - Same title, description, priority, and tags
    - New due date calculated based on recurrence pattern
    - Status set to pending
- Recurrence rules MUST be displayed in task details
- Recurrence MUST be editable (change pattern or remove recurrence)

##### Data Model Changes
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| recurrence | enum/null | No | null | One of: daily, weekly, monthly, or null (one-time) |
| recurrence_base_date | date/null | No | null | Original date for calculating next occurrence |

##### Recurrence Calculation Rules
- **Daily**: Next occurrence = current due_date + 1 day
- **Weekly**: Next occurrence = current due_date + 7 days
- **Monthly**: Next occurrence = current due_date + 1 month (same day, or last day of month if overflow)

##### Console (CLI) Behavior
- Create recurring task: `add "Daily standup" --due 2025-01-01 --recurrence daily`
- Update recurrence: `update <id> --recurrence weekly`
- Remove recurrence: `update <id> --recurrence none`
- Display format: `[ID] [PRIORITY] [STATUS] Title (repeats: daily) [due: 2025-01-01]`

##### Phase I Constraints
- Recurrence is triggered ONLY when user marks task as complete (no background scheduling)
- All recurrence logic executes synchronously during the complete operation
- No external scheduling or cron jobs

---

#### 2. Due Dates & Time Reminders

##### User Stories
- As a user, I want to set a due date for my tasks so I can track deadlines
- As a user, I want to set a specific time for my due date so I can be precise about deadlines
- As a user, I want to be warned if I try to set a due date in the past
- As a user, I want to see reminders for tasks that are due soon

##### Acceptance Criteria
- Due date MUST accept date in ISO format (YYYY-MM-DD)
- Due time MUST be optional and accept 24-hour format (HH:MM)
- Setting a due date/time in the past MUST be rejected with an error message
- Tasks MUST display due date and time in the task list
- Reminder logic MUST identify tasks due within a configurable threshold (default: 24 hours)
- Reminders MUST be displayed as console output (mocked notifications)
- Overdue tasks MUST be clearly indicated in the task list

##### Data Model Changes
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| due_date | date/null | No | null | Due date in YYYY-MM-DD format |
| due_time | time/null | No | null | Due time in HH:MM format (24-hour) |

##### Reminder Logic
- **Console reminder**: When listing tasks, display "[REMINDER]" prefix for tasks due within threshold
- **Overdue indicator**: Display "[OVERDUE]" prefix for tasks past their due date/time
- **Reminder threshold**: Configurable (default 24 hours, can be set to 1 hour, 12 hours, etc.)

##### Console (CLI) Behavior
- Set due date: `add "Submit report" --due 2025-01-15`
- Set due date and time: `add "Team meeting" --due 2025-01-15 --time 14:30`
- Update due date: `update <id> --due 2025-01-20`
- Check reminders: `reminders` (lists all tasks due within threshold)
- Configure threshold: `config reminder-threshold 12h`
- Display format: `[ID] [REMINDER] [PRIORITY] [STATUS] Title [due: 2025-01-15 14:30]`
- Overdue format: `[ID] [OVERDUE] [PRIORITY] [STATUS] Title [due: 2025-01-10 09:00]`

##### Validation Rules
- Due date MUST be today or in the future when setting (past dates rejected)
- Due time without due date MUST be rejected
- Invalid date/time formats MUST display helpful error messages

##### Phase I Constraints
- No push notifications or system alerts (console output only)
- No background workers checking for due tasks
- Reminders are checked on-demand when user runs `list` or `reminders` command
- All date/time validation occurs at input time, not via scheduled checks

---

## Additional Constraints

Technology stack requirements: UV, Python 3.13+, Claude Code, Spec-Kit Plus; In-memory storage only (no persistent database in Phase I); Console-based interface without web components; No external dependencies beyond those required for the specified stack; Code must be executable and functional on standard Python environments.

## Development Workflow

Specification-first approach: Write detailed specs → Generate plan → Break into tasks → Implement via Claude Code; No code implementation without approved specifications; All changes must follow the Agentic Dev Stack workflow (AGENTS.md + Spec-KitPlus + Claude Code); Each feature must be traceable back to a specific requirement in the specification.

## Governance

Constitution supersedes all other practices; Amendments require documentation, approval, migration plan; All PRs/reviews must verify compliance with spec-driven development; Complexity must be justified against the basic requirements; Use CLAUDE.md for runtime development guidance.

**Version**: 1.1.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-29
