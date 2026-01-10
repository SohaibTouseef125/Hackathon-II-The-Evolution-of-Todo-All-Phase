# Data Model: Phase 1 Todo In-Memory Python Console App

## Task Entity

**Attributes**:
- `id` (int): Unique identifier for the task (auto-generated)
- `title` (str): Title of the task (required, 1-200 characters)
- `description` (str): Optional description of the task (max 1000 characters)
- `completed` (bool): Completion status of the task (default: False)
- `created_at` (datetime): Timestamp when task was created

**Validation Rules**:
- Title must be 1-200 characters
- Description must be 0-1000 characters if provided
- ID must be unique within the task list
- Completed status must be boolean

**State Transitions**:
- Pending (completed=False) → Completed (completed=True) when marked complete
- Completed (completed=True) → Pending (completed=False) when marked incomplete

## TaskList Entity

**Attributes**:
- `tasks` (list): Collection of Task objects
- `next_id` (int): Counter for generating next unique ID

**Operations**:
- Add task: Creates new task with unique ID and adds to collection
- Get task by ID: Retrieves specific task from collection
- Update task: Modifies existing task properties
- Delete task: Removes task from collection
- List tasks: Returns all tasks or filtered subset
- Toggle completion: Changes completed status of specific task

**Validation Rules**:
- Task IDs must be unique within the list
- Operations must reference existing task IDs
- Maximum of 100 tasks allowed in memory