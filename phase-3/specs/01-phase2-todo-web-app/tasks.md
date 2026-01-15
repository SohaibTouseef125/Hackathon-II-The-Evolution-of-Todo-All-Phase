---
description: "Task list for Phase-2 Todo Web Application implementation"
---

# Tasks: Phase-2 Todo Web Application

**Input**: Design documents from `/specs/01-phase2-todo-web-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure with backend/ and frontend/ directories
- [X] T002 Initialize Python project with FastAPI, SQLModel, and Neon PostgreSQL dependencies in backend/
- [X] T003 [P] Initialize TypeScript/Next.js project with Tailwind CSS in frontend/
- [X] T004 [P] Configure linting and formatting tools for both frontend and backend

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Foundational tasks for the Todo Web Application:

- [X] T005 Setup database schema and migrations framework using SQLModel and Neon PostgreSQL in backend/
- [X] T006 [P] Implement authentication/authorization framework with Better Auth and JWT validation in both frontend and backend
- [X] T007 [P] Setup API routing and middleware structure in backend/
- [X] T008 Create base models/entities that all stories depend on (User and Task models) in backend/models.py
- [X] T009 Configure error handling and logging infrastructure in backend/
- [X] T010 Setup environment configuration management in both frontend and backend

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - New User Registration and Task Management (Priority: P1) 🎯 MVP

**Goal**: A new user can visit the Todo app website, create an account, and start managing their tasks. This includes the complete user onboarding flow and core functionality.

**Independent Test**: Can be fully tested by creating a new account, adding tasks, viewing them, and ensuring they persist after logout/login. Delivers the complete value proposition of the application.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T011 [P] [US1] Contract test for user registration endpoint in backend/tests/contract/test_auth.py
- [X] T012 [P] [US1] Integration test for user registration flow in backend/tests/integration/test_auth.py

### Implementation for User Story 1

- [X] T013 [P] [US1] Create User model in backend/models.py
- [X] T014 [US1] Create Task model in backend/models.py
- [X] T015 [US1] Implement user registration service in backend/services/user_service.py
- [X] T016 [US1] Implement authentication endpoints in backend/routes/auth.py
- [X] T017 [US1] Create signup page component in frontend/src/app/signup/page.tsx
- [X] T018 [US1] Create login page component in frontend/src/app/login/page.tsx
- [X] T019 [US1] Implement basic task creation endpoint in backend/routes/tasks.py
- [X] T020 [US1] Create task form component in frontend/src/components/task-form.tsx
- [X] T021 [US1] Add validation and error handling for user registration and task creation
- [X] T022 [US1] Add logging for user story 1 operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Operations (Priority: P1)

**Goal**: An authenticated user performs CRUD operations on their tasks: creating, viewing, updating, and deleting tasks, as well as marking them as complete/incomplete.

**Independent Test**: Can be tested by performing all CRUD operations on tasks and verifying they work correctly and persist in the database.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T023 [P] [US2] Contract test for task CRUD endpoints in backend/tests/contract/test_tasks.py
- [X] T024 [P] [US2] Integration test for task operations flow in backend/tests/integration/test_tasks.py

### Implementation for User Story 2

- [X] T025 [P] [US2] Implement task retrieval service in backend/services/task_service.py
- [X] T026 [US2] Implement task update service in backend/services/task_service.py
- [X] T027 [US2] Implement task deletion service in backend/services/task_service.py
- [X] T028 [US2] Implement task completion toggle service in backend/services/task_service.py
- [X] T029 [US2] Create task list component in frontend/src/components/task-list.tsx
- [X] T030 [US2] Create task detail/edit component in frontend/src/components/task-detail.tsx
- [X] T031 [US2] Implement task CRUD endpoints in backend/routes/tasks.py
- [X] T032 [US2] Create task management page in frontend/src/app/dashboard/page.tsx
- [X] T033 [US2] Integrate with User Story 1 authentication components

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Multi-User Data Isolation (Priority: P1)

**Goal**: Multiple users can use the application simultaneously, each seeing only their own tasks and unable to access others' data.

**Independent Test**: Can be tested by creating multiple user accounts and verifying that each user only sees their own tasks, even when using the same device or browser.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T034 [P] [US3] Contract test for user data isolation in backend/tests/contract/test_isolation.py
- [X] T035 [P] [US3] Integration test for multi-user access in backend/tests/integration/test_isolation.py

### Implementation for User Story 3

- [X] T036 [P] [US3] Implement user data isolation middleware in backend/middleware/auth.py
- [X] T037 [US3] Add user_id validation in all task endpoints to ensure users can only access their own tasks
- [X] T038 [US3] Implement JWT token validation to extract user_id for all protected endpoints
- [X] T039 [US3] Create user profile component in frontend/src/components/user-profile.tsx
- [X] T040 [US3] Add user-specific task filtering in frontend API client
- [X] T041 [US3] Add error handling for unauthorized access attempts

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T042 [P] Documentation updates in docs/
- [X] T043 Code cleanup and refactoring
- [X] T044 Performance optimization across all stories
- [X] T045 [P] Additional unit tests (if requested) in tests/unit/
- [X] T046 Security hardening
- [X] T047 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for user registration endpoint in backend/tests/contract/test_auth.py"
Task: "Integration test for user registration flow in backend/tests/integration/test_auth.py"

# Launch all models for User Story 1 together:
Task: "Create User model in backend/models.py"
Task: "Create Task model in backend/models.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence