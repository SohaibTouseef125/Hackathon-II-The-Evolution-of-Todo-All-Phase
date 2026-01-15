# Data Model: Phase-2 Todo Web Application

**Date**: 2026-01-03
**Feature**: Phase-2 Todo Web Application
**Branch**: 01-phase2-todo-web-app

## Entity Overview

This document defines the data models for the Phase-2 Todo Web Application, focusing on the task management functionality with user authentication and data isolation.

## Core Entities

### User

**Description**: Represents a registered user in the system
**Fields**:

- id (string): Unique identifier for the user (managed by Better Auth)
- email (string): User's email address (unique, required)
- name (string): User's display name (optional)
- created_at (datetime): Timestamp when user account was created
- updated_at (datetime): Timestamp when user account was last updated

**Relationships**:

- One-to-Many: User has many Tasks (via user_id foreign key)

**Validation Rules**:

- Email must be a valid email format
- Email must be unique across all users
- Name length must be between 1-100 characters if provided

### Task

**Description**: Represents a Todo item in the system
**Fields**:

- id (integer): Primary key, auto-incremented
- user_id (string): Foreign key linking to User (required)
- title (string): Task title (required, 1-200 characters)
- description (text): Task description (optional, max 1000 characters)
- completed (boolean): Task completion status (default: false)
- created_at (datetime): Timestamp when task was created
- updated_at (datetime): Timestamp when task was last updated

**Relationships**:

- Many-to-One: Task belongs to one User (via user_id)

**Validation Rules**:

- Title is required and must be 1-200 characters
- Description is optional and can be up to 1000 characters
- user_id must reference a valid User
- completed defaults to false when creating a new task

## State Transitions

### Task State Transitions

- **Created**: Task is initially created with completed = false
- **Updated**: Task details can be modified (title, description)
- **Completed**: Task status changes from false to true
- **Reopened**: Task status changes from true to false
- **Deleted**: Task is permanently removed from the system

## Data Relationships

### User-Task Relationship

```
User (1) ←→ (Many) Task
User.id ←→ Task.user_id (foreign key)
```

This relationship ensures proper data isolation where each user can only access their own tasks.

## Database Schema

### Tasks Table

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE
);
```

### Indexes

```sql
-- Index for efficient user-based task queries
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Index for filtering by completion status
CREATE INDEX idx_tasks_completed ON tasks(completed);

-- Composite index for common queries (user and status)
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
```

## API Data Transfer Objects (DTOs)

### TaskRequest

**Purpose**: Used for creating and updating tasks
**Fields**:

- title (string): Task title (required)
- description (string): Task description (optional)

### TaskResponse

**Purpose**: Used for API responses containing task data
**Fields**:

- id (integer): Task identifier
- user_id (string): User identifier
- title (string): Task title
- description (string): Task description
- completed (boolean): Completion status
- created_at (datetime): Creation timestamp
- updated_at (datetime): Last update timestamp

### TaskListResponse

**Purpose**: Used for API responses containing multiple tasks
**Fields**:

- tasks (array of TaskResponse): List of tasks
- total_count (integer): Total number of tasks
- completed_count (integer): Number of completed tasks
- pending_count (integer): Number of pending tasks

## Validation Rules

### Input Validation

- Task title: 1-200 characters, required
- Task description: 0-1000 characters, optional
- User ID: Must match authenticated user's ID
- Task ID: Must exist and belong to authenticated user

### Business Validation

- Users can only modify their own tasks
- Users cannot create tasks for other users
- Task completion status can be toggled by the owner
- Task deletion is only allowed by the owner

## Data Access Patterns

### Common Queries

1. **Get all tasks for a user**: SELECT * FROM tasks WHERE user_id = ?
2. **Get completed tasks for a user**: SELECT * FROM tasks WHERE user_id = ? AND completed = TRUE
3. **Get pending tasks for a user**: SELECT * FROM tasks WHERE user_id = ? AND completed = FALSE
4. **Get specific task**: SELECT * FROM tasks WHERE id = ? AND user_id = ?
5. **Update task**: UPDATE tasks SET title = ?, description = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ? AND user_id = ?

### Security Considerations

- All queries must filter by user_id to ensure data isolation
- No direct access to tasks without user_id verification
- Foreign key constraints to prevent orphaned tasks
- Cascade delete to remove tasks when user is deleted
