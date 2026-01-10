# Todo App CLI Contracts

## Command Structure
```
todo-app [command] [arguments] [options]
```

## Commands

### add
**Purpose**: Add a new task
**Arguments**:
- title (required): Task title (string, 1-200 characters)
**Options**:
- --description: Optional task description (string, 0-1000 characters)
**Output**: Task ID and confirmation message
**Error cases**: Invalid title length, system error

### list
**Purpose**: List all tasks
**Arguments**: None
**Options**:
- --status: Filter by status (all|pending|completed, default: all)
- --sort: Sort by (id|title|date, default: id)
**Output**: Formatted list of tasks with ID, title, status
**Error cases**: No tasks found (not an error), system error

### update
**Purpose**: Update an existing task
**Arguments**:
- id (required): Task ID (integer)
**Options**:
- --title: New task title (string, 1-200 characters)
- --description: New task description (string, 0-1000 characters)
**Output**: Confirmation message
**Error cases**: Task not found, invalid ID, invalid title/description length, system error

### delete
**Purpose**: Delete a task
**Arguments**:
- id (required): Task ID (integer)
**Output**: Confirmation message
**Error cases**: Task not found, invalid ID, system error

### complete
**Purpose**: Mark task as complete
**Arguments**:
- id (required): Task ID (integer)
**Output**: Confirmation message
**Error cases**: Task not found, invalid ID, system error

### incomplete
**Purpose**: Mark task as incomplete
**Arguments**:
- id (required): Task ID (integer)
**Output**: Confirmation message
**Error cases**: Task not found, invalid ID, system error