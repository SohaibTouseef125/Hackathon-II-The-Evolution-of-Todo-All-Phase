# Tasks: Phase 1 Extended Features

**Input**: Design documents from `/specs/002-phase1-extended/`
**Prerequisites**: plan.md ✅, spec.md ✅, data-model.md ✅, research.md ✅
**Branch**: `002-phase1-extended`
**Date**: 2025-12-29

**Tests**: TDD mandatory per constitution. Tests written FIRST, must FAIL before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1.1, US1.2, etc.)
- Include exact file paths in descriptions

## User Story Mapping

| Story ID | Spec Reference | Description | Priority |
|----------|----------------|-------------|----------|
| US1.1 | Story 1.1 | Assign Priority to Task | P1 |
| US1.2 | Story 1.2 | Categorize Tasks with Tags | P1 |
| US2.1 | Story 2.1 | Search Tasks by Keyword | P1 |
| US2.2 | Story 2.2 | Filter by Completion Status | P1 |
| US2.3 | Story 2.3 | Filter by Priority | P2 |
| US2.4 | Story 2.4 | Filter by Due Date | P3 |
| US3.1 | Story 3.1 | Sort by Due Date | P2 |
| US3.2 | Story 3.2 | Sort by Priority | P2 |
| US3.3 | Story 3.3 | Sort Alphabetically | P3 |
| US4.1 | Story 4.1 | Create Daily Recurring Task | P1 |
| US4.2 | Story 4.2 | Create Weekly Recurring Task | P1 |
| US4.3 | Story 4.3 | Create Monthly Recurring Task | P2 |
| US4.4 | Story 4.4 | Modify or Remove Recurrence | P2 |
| US5.1 | Story 5.1 | Set Due Date on Task | P1 |
| US5.2 | Story 5.2 | Set Due Time on Task | P2 |
| US5.3 | Story 5.3 | View Reminders for Due Tasks | P1 |
| US5.4 | Story 5.4 | Configure Reminder Threshold | P3 |

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per plan.md layout (src/, tests/, models/, services/, cli/)
- [x] T002 Initialize Python 3.13+ project with UV package manager and pyproject.toml
- [x] T003 [P] Create src/__init__.py with package initialization
- [x] T004 [P] Create src/models/__init__.py
- [x] T005 [P] Create src/services/__init__.py
- [x] T006 [P] Create src/cli/__init__.py
- [x] T007 [P] Create tests/__init__.py
- [x] T008 [P] Create tests/unit/__init__.py
- [x] T009 [P] Create tests/integration/__init__.py
- [x] T010 [P] Create tests/contract/__init__.py

**Checkpoint**: Project skeleton ready for implementation

---

## Phase 2: Foundational (Core Models - Blocking Prerequisites)

**Purpose**: Core data structures that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Tests for Foundational Phase (TDD - Write First, Must Fail)

- [x] T011 [P] Write failing tests for Priority enum in tests/unit/test_models.py
- [x] T012 [P] Write failing tests for Recurrence enum in tests/unit/test_models.py
- [x] T013 [P] Write failing tests for Task dataclass basic fields in tests/unit/test_models.py
- [x] T014 [P] Write failing tests for Config dataclass in tests/unit/test_models.py
- [x] T015 [P] Write failing tests for TaskStore CRUD in tests/unit/test_task_store.py

### Implementation for Foundational Phase

- [x] T016 Implement Priority enum (HIGH, MEDIUM, LOW) with sort_key() method in src/models/task.py
- [x] T017 Implement Recurrence enum (DAILY, WEEKLY, MONTHLY, NONE) in src/models/task.py
- [x] T018 Implement Task dataclass with all fields (id, title, description, completed, priority, tags, due_date, due_time, recurrence, created_at, updated_at) in src/models/task.py
- [x] T019 Implement Config dataclass with reminder_threshold (default 24h) in src/models/config.py
- [x] T020 Implement TaskStore class with add(), get(), update(), delete(), list_all() in src/services/task_store.py
- [x] T021 Run foundational tests - all must PASS before proceeding

**Checkpoint**: Foundation ready - user story implementation can begin

---

## Phase 3: User Story US1.1 - Assign Priority to Task (Priority: P1) 🎯 MVP

**Goal**: Users can assign priority levels (high, medium, low) to tasks

**Independent Test**: Create task with `--priority high`, verify `[HIGH]` displays in output

**Spec Reference**: FR-P001 through FR-P005

### Tests for US1.1 (TDD - Write First, Must Fail)

- [ ] T022 [P] [US1.1] Write failing test for priority set at creation in tests/unit/test_task_service.py
- [ ] T023 [P] [US1.1] Write failing test for priority defaults to medium in tests/unit/test_task_service.py
- [ ] T024 [P] [US1.1] Write failing test for priority update in tests/unit/test_task_service.py
- [ ] T025 [P] [US1.1] Write failing test for invalid priority error in tests/contract/test_validation.py
- [ ] T026 [P] [US1.1] Write failing test for priority display format in tests/unit/test_formatters.py

### Implementation for US1.1

- [ ] T027 [US1.1] Implement validate_priority() function in src/services/task_service.py
- [ ] T028 [US1.1] Add --priority argument to add subcommand in src/cli/parser.py
- [ ] T029 [US1.1] Add --priority argument to update subcommand in src/cli/parser.py
- [ ] T030 [US1.1] Implement priority display format `[HIGH]`, `[MEDIUM]`, `[LOW]` in src/cli/formatters.py
- [ ] T031 [US1.1] Implement add command handler with priority support in src/cli/commands.py
- [ ] T032 [US1.1] Implement update command handler with priority support in src/cli/commands.py
- [ ] T033 [US1.1] Run US1.1 tests - all must PASS

**Checkpoint**: Priority assignment fully functional

---

## Phase 4: User Story US1.2 - Categorize Tasks with Tags (Priority: P1)

**Goal**: Users can add tags/categories to tasks for organization

**Independent Test**: Create task with `--tags work,urgent`, verify `[tags: work, urgent]` displays

**Spec Reference**: FR-T001 through FR-T007

### Tests for US1.2 (TDD - Write First, Must Fail)

- [ ] T034 [P] [US1.2] Write failing test for tags set at creation in tests/unit/test_task_service.py
- [ ] T035 [P] [US1.2] Write failing test for tags update (replace) in tests/unit/test_task_service.py
- [ ] T036 [P] [US1.2] Write failing test for tags deduplicated and lowercased in tests/unit/test_task_service.py
- [ ] T037 [P] [US1.2] Write failing test for max 10 tags validation in tests/contract/test_validation.py
- [ ] T038 [P] [US1.2] Write failing test for invalid tag format in tests/contract/test_validation.py
- [ ] T039 [P] [US1.2] Write failing test for tags display format in tests/unit/test_formatters.py

### Implementation for US1.2

- [ ] T040 [US1.2] Implement validate_tags() function (lowercase, dedupe, max 10, regex) in src/services/task_service.py
- [ ] T041 [US1.2] Implement parse_tags() for comma-separated input in src/services/task_service.py
- [ ] T042 [US1.2] Add --tags argument to add subcommand in src/cli/parser.py
- [ ] T043 [US1.2] Add --tags argument to update subcommand in src/cli/parser.py
- [ ] T044 [US1.2] Implement tags display format `[tags: tag1, tag2]` in src/cli/formatters.py
- [ ] T045 [US1.2] Update add command handler with tags support in src/cli/commands.py
- [ ] T046 [US1.2] Update update command handler with tags support in src/cli/commands.py
- [ ] T047 [US1.2] Run US1.2 tests - all must PASS

**Checkpoint**: Tag categorization fully functional

---

## Phase 5: User Story US5.1 - Set Due Date on Task (Priority: P1)

**Goal**: Users can set due dates for deadline tracking

**Independent Test**: Create task with `--due 2025-01-15`, verify `[due: 2025-01-15]` displays

**Spec Reference**: FR-D001 through FR-D007

**Note**: Due dates needed before filters (US2.4) and sort (US3.1) can be implemented

### Tests for US5.1 (TDD - Write First, Must Fail)

- [ ] T048 [P] [US5.1] Write failing test for due date set in YYYY-MM-DD format in tests/unit/test_task_service.py
- [ ] T049 [P] [US5.1] Write failing test for past dates rejected in tests/contract/test_validation.py
- [ ] T050 [P] [US5.1] Write failing test for invalid date format error in tests/contract/test_validation.py
- [ ] T051 [P] [US5.1] Write failing test for due date updateable in tests/unit/test_task_service.py
- [ ] T052 [P] [US5.1] Write failing test for due date removable with "none" in tests/unit/test_task_service.py
- [ ] T053 [P] [US5.1] Write failing test for due date display format in tests/unit/test_formatters.py

### Implementation for US5.1

- [ ] T054 [US5.1] Implement validate_due_date() function in src/services/task_service.py
- [ ] T055 [US5.1] Add --due argument (YYYY-MM-DD or "none") to add subcommand in src/cli/parser.py
- [ ] T056 [US5.1] Add --due argument to update subcommand in src/cli/parser.py
- [ ] T057 [US5.1] Implement due date display format `[due: YYYY-MM-DD]` in src/cli/formatters.py
- [ ] T058 [US5.1] Update add command handler with due date support in src/cli/commands.py
- [ ] T059 [US5.1] Update update command handler with due date support in src/cli/commands.py
- [ ] T060 [US5.1] Run US5.1 tests - all must PASS

**Checkpoint**: Due date tracking fully functional

---

## Phase 6: User Story US5.2 - Set Due Time on Task (Priority: P2)

**Goal**: Users can set specific time for due dates

**Independent Test**: Create task with `--due 2025-01-15 --time 14:30`, verify `[due: 2025-01-15 14:30]` displays

**Spec Reference**: FR-D002, FR-D004, FR-D005

### Tests for US5.2 (TDD - Write First, Must Fail)

- [ ] T061 [P] [US5.2] Write failing test for due time set in HH:MM format in tests/unit/test_task_service.py
- [ ] T062 [P] [US5.2] Write failing test for time without date rejected in tests/contract/test_validation.py
- [ ] T063 [P] [US5.2] Write failing test for invalid time format error in tests/contract/test_validation.py
- [ ] T064 [P] [US5.2] Write failing test for due time display format in tests/unit/test_formatters.py

### Implementation for US5.2

- [ ] T065 [US5.2] Implement validate_due_time() function in src/services/task_service.py
- [ ] T066 [US5.2] Add --time argument (HH:MM) to add subcommand in src/cli/parser.py
- [ ] T067 [US5.2] Add --time argument to update subcommand in src/cli/parser.py
- [ ] T068 [US5.2] Update due display format `[due: YYYY-MM-DD HH:MM]` in src/cli/formatters.py
- [ ] T069 [US5.2] Update add command handler with time support in src/cli/commands.py
- [ ] T070 [US5.2] Update update command handler with time support in src/cli/commands.py
- [ ] T071 [US5.2] Run US5.2 tests - all must PASS

**Checkpoint**: Due time tracking fully functional

---

## Phase 7: User Story US2.1 - Search Tasks by Keyword (Priority: P1)

**Goal**: Users can search tasks by keyword in title/description

**Independent Test**: Create tasks, run `search "report"`, verify matching tasks displayed

**Spec Reference**: FR-S001 through FR-S004

### Tests for US2.1 (TDD - Write First, Must Fail)

- [ ] T072 [P] [US2.1] Write failing test for search matches title (case-insensitive) in tests/unit/test_task_service.py
- [ ] T073 [P] [US2.1] Write failing test for search matches description in tests/unit/test_task_service.py
- [ ] T074 [P] [US2.1] Write failing test for search partial match in tests/unit/test_task_service.py
- [ ] T075 [P] [US2.1] Write failing test for empty search results message in tests/unit/test_task_service.py
- [ ] T076 [P] [US2.1] Write failing test for search result count display in tests/unit/test_formatters.py

### Implementation for US2.1

- [ ] T077 [US2.1] Implement search_tasks() function in src/services/task_service.py
- [ ] T078 [US2.1] Add search subcommand with keyword argument in src/cli/parser.py
- [ ] T079 [US2.1] Implement search command handler in src/cli/commands.py
- [ ] T080 [US2.1] Implement search results formatter with count in src/cli/formatters.py
- [ ] T081 [US2.1] Run US2.1 tests - all must PASS

**Checkpoint**: Keyword search fully functional

---

## Phase 8: User Story US2.2 - Filter by Completion Status (Priority: P1)

**Goal**: Users can filter tasks by pending/completed status

**Independent Test**: Create tasks, complete some, run `list --status pending`, verify only pending shown

**Spec Reference**: FR-F001

### Tests for US2.2 (TDD - Write First, Must Fail)

- [ ] T082 [P] [US2.2] Write failing test for filter by status pending in tests/unit/test_task_service.py
- [ ] T083 [P] [US2.2] Write failing test for filter by status completed in tests/unit/test_task_service.py
- [ ] T084 [P] [US2.2] Write failing test for filter by status all in tests/unit/test_task_service.py
- [ ] T085 [P] [US2.2] Write failing test for empty filter results message in tests/unit/test_task_service.py

### Implementation for US2.2

- [ ] T086 [US2.2] Implement filter_by_status() function in src/services/task_service.py
- [ ] T087 [US2.2] Add --status argument (pending, completed, all) to list subcommand in src/cli/parser.py
- [ ] T088 [US2.2] Update list command handler with status filter in src/cli/commands.py
- [ ] T089 [US2.2] Run US2.2 tests - all must PASS

**Checkpoint**: Status filtering fully functional

---

## Phase 9: User Story US2.3 - Filter by Priority (Priority: P2)

**Goal**: Users can filter tasks by priority level

**Independent Test**: Create tasks with different priorities, run `list --priority high`, verify only high shown

**Spec Reference**: FR-F002

### Tests for US2.3 (TDD - Write First, Must Fail)

- [ ] T090 [P] [US2.3] Write failing test for filter by priority high in tests/unit/test_task_service.py
- [ ] T091 [P] [US2.3] Write failing test for filter by priority medium in tests/unit/test_task_service.py
- [ ] T092 [P] [US2.3] Write failing test for filter by priority low in tests/unit/test_task_service.py
- [ ] T093 [P] [US2.3] Write failing test for combined status + priority filter in tests/unit/test_task_service.py

### Implementation for US2.3

- [ ] T094 [US2.3] Implement filter_by_priority() function in src/services/task_service.py
- [ ] T095 [US2.3] Add --priority argument to list subcommand in src/cli/parser.py
- [ ] T096 [US2.3] Update list command handler with priority filter in src/cli/commands.py
- [ ] T097 [US2.3] Run US2.3 tests - all must PASS

**Checkpoint**: Priority filtering fully functional

---

## Phase 10: User Story US2.4 - Filter by Due Date (Priority: P3)

**Goal**: Users can filter tasks by due date (today, week, overdue)

**Independent Test**: Create tasks with due dates, run `list --due today`, verify only today's tasks shown

**Spec Reference**: FR-F003

**Dependencies**: Requires US5.1 (Due Dates) to be complete

### Tests for US2.4 (TDD - Write First, Must Fail)

- [ ] T098 [P] [US2.4] Write failing test for filter by due today in tests/unit/test_task_service.py
- [ ] T099 [P] [US2.4] Write failing test for filter by due week in tests/unit/test_task_service.py
- [ ] T100 [P] [US2.4] Write failing test for filter by due overdue in tests/unit/test_task_service.py
- [ ] T101 [P] [US2.4] Write failing test for combined status + priority + due filter in tests/unit/test_task_service.py

### Implementation for US2.4

- [ ] T102 [US2.4] Implement filter_by_due_date() function in src/services/task_service.py
- [ ] T103 [US2.4] Add --due argument (today, week, overdue, all) to list subcommand in src/cli/parser.py
- [ ] T104 [US2.4] Update list command handler with due date filter in src/cli/commands.py
- [ ] T105 [US2.4] Run US2.4 tests - all must PASS

**Checkpoint**: Due date filtering fully functional

---

## Phase 11: User Story US3.1 - Sort by Due Date (Priority: P2)

**Goal**: Users can sort tasks by due date (earliest first)

**Independent Test**: Create tasks with different due dates, run `list --sort due_date`, verify ordered by date

**Spec Reference**: FR-SO001, FR-SO003, FR-SO006

**Dependencies**: Requires US5.1 (Due Dates) to be complete

### Tests for US3.1 (TDD - Write First, Must Fail)

- [ ] T106 [P] [US3.1] Write failing test for sort by due_date ascending in tests/unit/test_task_service.py
- [ ] T107 [P] [US3.1] Write failing test for sort by due_date descending (--reverse) in tests/unit/test_task_service.py
- [ ] T108 [P] [US3.1] Write failing test for tasks without due date at end in tests/unit/test_task_service.py

### Implementation for US3.1

- [ ] T109 [US3.1] Implement sort_by_due_date() function in src/services/task_service.py
- [ ] T110 [US3.1] Add --sort argument with due_date choice to list subcommand in src/cli/parser.py
- [ ] T111 [US3.1] Add --reverse flag to list subcommand in src/cli/parser.py
- [ ] T112 [US3.1] Update list command handler with sort support in src/cli/commands.py
- [ ] T113 [US3.1] Run US3.1 tests - all must PASS

**Checkpoint**: Due date sorting fully functional

---

## Phase 12: User Story US3.2 - Sort by Priority (Priority: P2)

**Goal**: Users can sort tasks by priority (high first)

**Independent Test**: Create tasks with different priorities, run `list --sort priority`, verify ordered high → medium → low

**Spec Reference**: FR-SO001, FR-SO003, FR-SO005

### Tests for US3.2 (TDD - Write First, Must Fail)

- [ ] T114 [P] [US3.2] Write failing test for sort by priority ascending (high first) in tests/unit/test_task_service.py
- [ ] T115 [P] [US3.2] Write failing test for sort by priority descending (low first) in tests/unit/test_task_service.py
- [ ] T116 [P] [US3.2] Write failing test for sort + filter combined in tests/unit/test_task_service.py

### Implementation for US3.2

- [ ] T117 [US3.2] Implement sort_by_priority() function in src/services/task_service.py
- [ ] T118 [US3.2] Add priority choice to --sort argument in src/cli/parser.py
- [ ] T119 [US3.2] Update list command handler with priority sort in src/cli/commands.py
- [ ] T120 [US3.2] Run US3.2 tests - all must PASS

**Checkpoint**: Priority sorting fully functional

---

## Phase 13: User Story US3.3 - Sort Alphabetically (Priority: P3)

**Goal**: Users can sort tasks alphabetically by title

**Independent Test**: Create multiple tasks, run `list --sort title`, verify A-Z order

**Spec Reference**: FR-SO001, FR-SO003, FR-SO007

### Tests for US3.3 (TDD - Write First, Must Fail)

- [ ] T121 [P] [US3.3] Write failing test for sort by title A-Z in tests/unit/test_task_service.py
- [ ] T122 [P] [US3.3] Write failing test for sort by title Z-A (--reverse) in tests/unit/test_task_service.py
- [ ] T123 [P] [US3.3] Write failing test for case-insensitive alphabetical sort in tests/unit/test_task_service.py

### Implementation for US3.3

- [ ] T124 [US3.3] Implement sort_by_title() function in src/services/task_service.py
- [ ] T125 [US3.3] Add title choice to --sort argument in src/cli/parser.py
- [ ] T126 [US3.3] Update list command handler with title sort in src/cli/commands.py
- [ ] T127 [US3.3] Add created choice to --sort as default in src/cli/parser.py
- [ ] T128 [US3.3] Run US3.3 tests - all must PASS

**Checkpoint**: All sorting fully functional

---

## Phase 14: User Story US5.3 - View Reminders for Due Tasks (Priority: P1)

**Goal**: Users see visual indicators for upcoming/overdue tasks

**Independent Test**: Create task due within 24h, run `list`, verify `[REMINDER]` prefix displayed

**Spec Reference**: FR-REM001 through FR-REM005, FR-REM008

**Dependencies**: Requires US5.1 (Due Dates) to be complete

### Tests for US5.3 (TDD - Write First, Must Fail)

- [ ] T129 [P] [US5.3] Write failing test for is_overdue computed property in tests/unit/test_models.py
- [ ] T130 [P] [US5.3] Write failing test for is_reminder computed property in tests/unit/test_models.py
- [ ] T131 [P] [US5.3] Write failing test for [OVERDUE] prefix display in tests/unit/test_formatters.py
- [ ] T132 [P] [US5.3] Write failing test for [REMINDER] prefix display in tests/unit/test_formatters.py
- [ ] T133 [P] [US5.3] Write failing test for reminders command in tests/unit/test_task_service.py

### Implementation for US5.3

- [ ] T134 [US5.3] Implement _get_due_datetime() helper method in src/models/task.py
- [ ] T135 [US5.3] Implement is_overdue property in src/models/task.py
- [ ] T136 [US5.3] Implement is_reminder property in src/models/task.py
- [ ] T137 [US5.3] Update format_display() with [OVERDUE] and [REMINDER] prefixes in src/cli/formatters.py
- [ ] T138 [US5.3] Add reminders subcommand in src/cli/parser.py
- [ ] T139 [US5.3] Implement get_reminder_tasks() function in src/services/task_service.py
- [ ] T140 [US5.3] Implement reminders command handler in src/cli/commands.py
- [ ] T141 [US5.3] Run US5.3 tests - all must PASS

**Checkpoint**: Reminder indicators fully functional

---

## Phase 15: User Story US5.4 - Configure Reminder Threshold (Priority: P3)

**Goal**: Users can configure the reminder threshold

**Independent Test**: Run `config reminder-threshold 12h`, create task due in 10h, verify `[REMINDER]` shown

**Spec Reference**: FR-REM006, FR-REM007

### Tests for US5.4 (TDD - Write First, Must Fail)

- [ ] T142 [P] [US5.4] Write failing test for threshold parsing (1h, 6h, 12h, 24h, 48h, 7d) in tests/unit/test_models.py
- [ ] T143 [P] [US5.4] Write failing test for invalid threshold format error in tests/contract/test_validation.py
- [ ] T144 [P] [US5.4] Write failing test for config display current settings in tests/unit/test_task_service.py

### Implementation for US5.4

- [ ] T145 [US5.4] Implement set_threshold() method in src/models/config.py
- [ ] T146 [US5.4] Implement get_threshold_display() method in src/models/config.py
- [ ] T147 [US5.4] Add config subcommand with reminder-threshold argument in src/cli/parser.py
- [ ] T148 [US5.4] Implement config command handler in src/cli/commands.py
- [ ] T149 [US5.4] Run US5.4 tests - all must PASS

**Checkpoint**: Reminder configuration fully functional

---

## Phase 16: User Story US4.1 - Create Daily Recurring Task (Priority: P1)

**Goal**: Users can create tasks that repeat daily

**Independent Test**: Create task with `--recurrence daily --due 2025-01-01`, complete it, verify new task with due 2025-01-02 created

**Spec Reference**: FR-R001, FR-R003, FR-R004, FR-R005, FR-R006, FR-R007, FR-R010, FR-R012

**Dependencies**: Requires US5.1 (Due Dates) to be complete

### Tests for US4.1 (TDD - Write First, Must Fail)

- [ ] T150 [P] [US4.1] Write failing test for daily recurrence display in tests/unit/test_formatters.py
- [ ] T151 [P] [US4.1] Write failing test for recurrence requires due_date in tests/contract/test_validation.py
- [ ] T152 [P] [US4.1] Write failing test for calculate_next_due_date daily in tests/unit/test_recurrence.py
- [ ] T153 [P] [US4.1] Write failing test for complete triggers new task creation in tests/unit/test_task_service.py
- [ ] T154 [P] [US4.1] Write failing test for new task copies title, description, priority, tags in tests/unit/test_task_service.py

### Implementation for US4.1

- [ ] T155 [US4.1] Implement calculate_next_due_date() for DAILY in src/services/recurrence.py
- [ ] T156 [US4.1] Add --recurrence argument to add subcommand in src/cli/parser.py
- [ ] T157 [US4.1] Add recurrence validation (requires due_date) in src/services/task_service.py
- [ ] T158 [US4.1] Implement recurrence display format `(repeats: daily)` in src/cli/formatters.py
- [ ] T159 [US4.1] Implement complete_task() with recurrence handling in src/services/task_service.py
- [ ] T160 [US4.1] Update complete command handler with recurrence output in src/cli/commands.py
- [ ] T161 [US4.1] Run US4.1 tests - all must PASS

**Checkpoint**: Daily recurrence fully functional

---

## Phase 17: User Story US4.2 - Create Weekly Recurring Task (Priority: P1)

**Goal**: Users can create tasks that repeat weekly

**Independent Test**: Create task with `--recurrence weekly --due 2025-01-01`, complete it, verify new task with due 2025-01-08 created

**Spec Reference**: FR-R001, FR-R008

### Tests for US4.2 (TDD - Write First, Must Fail)

- [ ] T162 [P] [US4.2] Write failing test for calculate_next_due_date weekly (+7 days) in tests/unit/test_recurrence.py
- [ ] T163 [P] [US4.2] Write failing test for weekly recurrence display in tests/unit/test_formatters.py

### Implementation for US4.2

- [ ] T164 [US4.2] Implement calculate_next_due_date() for WEEKLY in src/services/recurrence.py
- [ ] T165 [US4.2] Update recurrence display format `(repeats: weekly)` in src/cli/formatters.py
- [ ] T166 [US4.2] Run US4.2 tests - all must PASS

**Checkpoint**: Weekly recurrence fully functional

---

## Phase 18: User Story US4.3 - Create Monthly Recurring Task (Priority: P2)

**Goal**: Users can create tasks that repeat monthly with edge case handling

**Independent Test**: Create task with `--recurrence monthly --due 2025-01-31`, complete it, verify new task with due 2025-02-28 created

**Spec Reference**: FR-R001, FR-R009

### Tests for US4.3 (TDD - Write First, Must Fail)

- [ ] T167 [P] [US4.3] Write failing test for calculate_next_due_date monthly (+1 month) in tests/unit/test_recurrence.py
- [ ] T168 [P] [US4.3] Write failing test for Jan 31 → Feb 28 edge case in tests/unit/test_recurrence.py
- [ ] T169 [P] [US4.3] Write failing test for Jan 30 → Feb 28 edge case in tests/unit/test_recurrence.py
- [ ] T170 [P] [US4.3] Write failing test for March 31 → April 30 edge case in tests/unit/test_recurrence.py
- [ ] T171 [P] [US4.3] Write failing test for monthly recurrence display in tests/unit/test_formatters.py

### Implementation for US4.3

- [ ] T172 [US4.3] Implement calculate_next_due_date() for MONTHLY with day clamping in src/services/recurrence.py
- [ ] T173 [US4.3] Update recurrence display format `(repeats: monthly)` in src/cli/formatters.py
- [ ] T174 [US4.3] Run US4.3 tests - all must PASS

**Checkpoint**: Monthly recurrence with edge cases fully functional

---

## Phase 19: User Story US4.4 - Modify or Remove Recurrence (Priority: P2)

**Goal**: Users can change or remove recurrence from tasks

**Independent Test**: Update recurring task with `--recurrence none`, complete it, verify no new task created

**Spec Reference**: FR-R011

### Tests for US4.4 (TDD - Write First, Must Fail)

- [ ] T175 [P] [US4.4] Write failing test for recurrence update from daily to weekly in tests/unit/test_task_service.py
- [ ] T176 [P] [US4.4] Write failing test for recurrence removal (--recurrence none) in tests/unit/test_task_service.py
- [ ] T177 [P] [US4.4] Write failing test for adding recurrence to one-time task in tests/unit/test_task_service.py

### Implementation for US4.4

- [ ] T178 [US4.4] Add --recurrence argument to update subcommand in src/cli/parser.py
- [ ] T179 [US4.4] Update update command handler with recurrence modification in src/cli/commands.py
- [ ] T180 [US4.4] Run US4.4 tests - all must PASS

**Checkpoint**: Recurrence modification fully functional

---

## Phase 20: Polish & Cross-Cutting Concerns

**Purpose**: Integration testing, CLI entry point, and final polish

- [ ] T181 [P] Create main.py CLI entry point with argparse setup in src/main.py
- [ ] T182 [P] Write integration tests for add command in tests/integration/test_cli.py
- [ ] T183 [P] Write integration tests for update command in tests/integration/test_cli.py
- [ ] T184 [P] Write integration tests for list command with filters in tests/integration/test_cli.py
- [ ] T185 [P] Write integration tests for search command in tests/integration/test_cli.py
- [ ] T186 [P] Write integration tests for complete command with recurrence in tests/integration/test_cli.py
- [ ] T187 [P] Write integration tests for reminders command in tests/integration/test_cli.py
- [ ] T188 [P] Write integration tests for config command in tests/integration/test_cli.py
- [ ] T189 Run full test suite - all tests must PASS
- [ ] T190 Verify all error messages match specification in plan.md

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup
    ↓
Phase 2: Foundational (BLOCKS all user stories)
    ↓
├── Phase 3: US1.1 Priority (can start immediately after Phase 2)
├── Phase 4: US1.2 Tags (can start immediately after Phase 2)
├── Phase 5: US5.1 Due Dates (can start immediately after Phase 2)
│   ↓
│   ├── Phase 6: US5.2 Due Time (depends on US5.1)
│   ├── Phase 7: US2.1 Search (can start after Phase 2)
│   ├── Phase 8: US2.2 Status Filter (can start after Phase 2)
│   ├── Phase 9: US2.3 Priority Filter (can start after Phase 2)
│   ├── Phase 10: US2.4 Due Date Filter (depends on US5.1)
│   ├── Phase 11: US3.1 Due Date Sort (depends on US5.1)
│   ├── Phase 12: US3.2 Priority Sort (can start after Phase 2)
│   ├── Phase 13: US3.3 Title Sort (can start after Phase 2)
│   ├── Phase 14: US5.3 Reminders (depends on US5.1)
│   ├── Phase 15: US5.4 Reminder Config (depends on US5.3)
│   └── Phase 16-19: US4.x Recurring (depends on US5.1)
    ↓
Phase 20: Polish (depends on all user stories)
```

### User Story Dependencies

| Story | Depends On | Can Run In Parallel With |
|-------|------------|-------------------------|
| US1.1 Priority | Phase 2 | US1.2, US5.1, US2.1, US2.2 |
| US1.2 Tags | Phase 2 | US1.1, US5.1, US2.1, US2.2 |
| US5.1 Due Dates | Phase 2 | US1.1, US1.2, US2.1, US2.2 |
| US5.2 Due Time | US5.1 | US2.3, US2.4, US3.x |
| US2.1 Search | Phase 2 | US1.1, US1.2, US5.1 |
| US2.2 Status Filter | Phase 2 | US1.1, US1.2, US5.1 |
| US2.3 Priority Filter | Phase 2 | US2.2, US5.1 |
| US2.4 Due Date Filter | US5.1 | US2.3, US3.1 |
| US3.1 Due Date Sort | US5.1 | US2.4, US3.2 |
| US3.2 Priority Sort | Phase 2 | US3.1, US3.3 |
| US3.3 Title Sort | Phase 2 | US3.1, US3.2 |
| US5.3 Reminders | US5.1 | US3.x, US4.x |
| US5.4 Reminder Config | US5.3 | US4.x |
| US4.1 Daily Recurring | US5.1 | US5.3, US4.2 |
| US4.2 Weekly Recurring | US4.1 | US4.3 |
| US4.3 Monthly Recurring | US4.2 | US4.4 |
| US4.4 Modify Recurrence | US4.1 | US4.3 |

---

## Parallel Execution Examples

### After Phase 2 Completion (Maximum Parallelism)

```bash
# These can all run in parallel:
Task: "T022-T033 US1.1 Priority" (5 tests + 7 implementation)
Task: "T034-T047 US1.2 Tags" (6 tests + 8 implementation)
Task: "T048-T060 US5.1 Due Dates" (6 tests + 7 implementation)
Task: "T072-T081 US2.1 Search" (5 tests + 5 implementation)
Task: "T082-T089 US2.2 Status Filter" (4 tests + 4 implementation)
```

### Within User Story (Parallel Tests)

```bash
# All tests for US1.1 can run in parallel:
Task: "T022 [P] [US1.1] Write failing test for priority set at creation"
Task: "T023 [P] [US1.1] Write failing test for priority defaults to medium"
Task: "T024 [P] [US1.1] Write failing test for priority update"
Task: "T025 [P] [US1.1] Write failing test for invalid priority error"
Task: "T026 [P] [US1.1] Write failing test for priority display format"
```

---

## Implementation Strategy

### MVP First (P1 Stories Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: US1.1 Priority ← **MVP Start**
4. Complete Phase 4: US1.2 Tags
5. Complete Phase 5: US5.1 Due Dates
6. Complete Phase 7: US2.1 Search
7. Complete Phase 8: US2.2 Status Filter
8. Complete Phase 14: US5.3 Reminders
9. Complete Phase 16: US4.1 Daily Recurring
10. Complete Phase 17: US4.2 Weekly Recurring
11. **STOP and VALIDATE**: All P1 stories functional

### Incremental Delivery

1. **Foundation** → Setup + Foundational complete
2. **MVP** → P1 stories complete → Deploy/Demo
3. **P2 Features** → US2.3, US3.1, US3.2, US4.3, US4.4, US5.2 → Deploy/Demo
4. **P3 Features** → US2.4, US3.3, US5.4 → Deploy/Demo
5. **Polish** → Integration tests, final validation → Release

---

## Summary

| Metric | Count |
|--------|-------|
| Total Tasks | 190 |
| Setup Tasks | 10 |
| Foundational Tasks | 11 |
| User Story Tasks | 159 |
| Polish Tasks | 10 |
| Test Tasks (TDD) | 85 |
| Implementation Tasks | 95 |
| Parallelizable Tasks | ~120 |
| User Stories | 17 |

**Ready for /sp.implement**
