# Skill Folder: in-memory-storage

## File: SKILL.md

```markdown
---
name: in-memory-storage
description: Implement CRUD operations using Python dictionaries and dataclasses for in-memory data storage. Use when building console apps, prototypes, or applications that don't need persistent database storage.
---

# In-Memory Storage Skill

## Purpose
Create efficient in-memory data storage using Python data structures with full CRUD (Create, Read, Update, Delete) operations.

## When to Use This Skill
- Building console applications without database
- Creating prototypes or MVPs
- Testing business logic without database
- Need fast, temporary data storage
- Learning CRUD patterns

## Core Pattern: Storage Class

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Task:
    """Task data model"""
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

class TaskStore:
    """In-memory task storage with CRUD operations"""
    
    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1
    
    # CREATE
    def add(self, title: str, description: Optional[str] = None) -> Task:
        """Add a new task"""
        task = Task(
            id=self._next_id,
            title=title,
            description=description
        )
        self._tasks[task.id] = task
        self._next_id += 1
        return task
    
    # READ
    def get(self, task_id: int) -> Optional[Task]:
        """Get task by ID"""
        return self._tasks.get(task_id)
    
    def get_all(self) -> List[Task]:
        """Get all tasks"""
        return list(self._tasks.values())
    
    def get_by_status(self, completed: bool) -> List[Task]:
        """Get tasks filtered by completion status"""
        return [
            task for task in self._tasks.values()
            if task.completed == completed
        ]
    
    # UPDATE
    def update(self, task_id: int, title: Optional[str] = None,
               description: Optional[str] = None) -> Optional[Task]:
        """Update task details"""
        task = self._tasks.get(task_id)
        if not task:
            return None
        
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        
        task.updated_at = datetime.now()
        return task
    
    def toggle_complete(self, task_id: int) -> Optional[Task]:
        """Toggle completion status"""
        task = self._tasks.get(task_id)
        if not task:
            return None
        
        task.completed = not task.completed
        task.updated_at = datetime.now()
        return task
    
    # DELETE
    def delete(self, task_id: int) -> bool:
        """Delete a task"""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
    
    # UTILITIES
    def count(self) -> int:
        """Get total number of tasks"""
        return len(self._tasks)
    
    def clear(self):
        """Clear all tasks"""
        self._tasks.clear()
        self._next_id = 1
```

## Singleton Pattern for Global Access

```python
# storage.py
_store: Optional[TaskStore] = None

def get_store() -> TaskStore:
    """Get or create the global store instance"""
    global _store
    if _store is None:
        _store = TaskStore()
    return _store

# Usage in other files
from storage import get_store

store = get_store()
task = store.add("Buy milk")
```

## Service Layer Pattern

Separate business logic from storage:

```python
class TaskService:
    """Business logic for task operations"""
    
    def __init__(self, store: TaskStore):
        self.store = store
    
    def create_task(self, title: str, description: str = "") -> Task:
        """Create task with validation"""
        # Validation
        if not title or len(title) > 200:
            raise ValueError("Title must be 1-200 characters")
        
        if len(description) > 1000:
            raise ValueError("Description max 1000 characters")
        
        # Create
        return self.store.add(title, description or None)
    
    def list_tasks(self, filter_by: Optional[str] = None) -> List[Task]:
        """List tasks with optional filter"""
        if filter_by == "completed":
            return self.store.get_by_status(True)
        elif filter_by == "pending":
            return self.store.get_by_status(False)
        else:
            return self.store.get_all()
    
    def get_task(self, task_id: int) -> Task:
        """Get task or raise error"""
        task = self.store.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        return task
    
    def update_task(self, task_id: int, title: Optional[str] = None,
                   description: Optional[str] = None) -> Task:
        """Update task with validation"""
        # Validate
        if title is not None and (not title or len(title) > 200):
            raise ValueError("Title must be 1-200 characters")
        
        # Update
        task = self.store.update(task_id, title, description)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        return task
    
    def mark_complete(self, task_id: int) -> Task:
        """Mark task as complete"""
        task = self.store.toggle_complete(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        return task
    
    def delete_task(self, task_id: int):
        """Delete task or raise error"""
        if not self.store.delete(task_id):
            raise ValueError(f"Task {task_id} not found")
```

## Advanced Patterns

### Sorting and Filtering
```python
def get_sorted_tasks(self, sort_by: str = "created") -> List[Task]:
    """Get tasks sorted by field"""
    tasks = self.get_all()
    
    if sort_by == "created":
        return sorted(tasks, key=lambda t: t.created_at)
    elif sort_by == "title":
        return sorted(tasks, key=lambda t: t.title.lower())
    elif sort_by == "updated":
        return sorted(tasks, key=lambda t: t.updated_at, reverse=True)
    
    return tasks

def search_tasks(self, query: str) -> List[Task]:
    """Search tasks by title or description"""
    query_lower = query.lower()
    return [
        task for task in self.get_all()
        if query_lower in task.title.lower() or
           (task.description and query_lower in task.description.lower())
    ]
```

### Serialization
```python
def to_dict(self) -> dict:
    """Convert task to dictionary"""
    return {
        'id': self.id,
        'title': self.title,
        'description': self.description,
        'completed': self.completed,
        'created_at': self.created_at.isoformat(),
        'updated_at': self.updated_at.isoformat()
    }

def export_all(self) -> list[dict]:
    """Export all tasks as dictionaries"""
    return [task.to_dict() for task in self.get_all()]
```

## Testing In-Memory Storage

```python
import pytest

@pytest.fixture
def store():
    """Create fresh store for each test"""
    store = TaskStore()
    yield store
    store.clear()

def test_add_task(store):
    """Test adding a task"""
    task = store.add("Test Task", "Description")
    
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Description"
    assert task.completed is False

def test_get_task(store):
    """Test retrieving a task"""
    task = store.add("Test")
    retrieved = store.get(task.id)
    
    assert retrieved is not None
    assert retrieved.id == task.id
    assert retrieved.title == task.title

def test_update_task(store):
    """Test updating a task"""
    task = store.add("Original")
    updated = store.update(task.id, title="Updated")
    
    assert updated is not None
    assert updated.title == "Updated"
    assert updated.id == task.id

def test_delete_task(store):
    """Test deleting a task"""
    task = store.add("To Delete")
    
    assert store.delete(task.id) is True
    assert store.get(task.id) is None
    assert store.delete(task.id) is False  # Already deleted

def test_filter_by_status(store):
    """Test filtering tasks"""
    task1 = store.add("Incomplete")
    task2 = store.add("Complete")
    store.toggle_complete(task2.id)
    
    pending = store.get_by_status(False)
    completed = store.get_by_status(True)
    
    assert len(pending) == 1
    assert len(completed) == 1
    assert task1 in pending
    assert task2 in completed
```

## Best Practices

1. **Use Dataclasses** - Clean, automatic __init__ and __repr__
2. **Separate Storage from Logic** - Store does storage, Service does validation
3. **Return Copies** - If needed, return copies not references to prevent external modification
4. **Handle Not Found** - Return None or raise clear exceptions
5. **Type Hints** - Use them everywhere for clarity
6. **Auto-timestamps** - Set created_at/updated_at automatically
7. **Unique IDs** - Use auto-increment for simplicity

## Common Pitfalls to Avoid
- Don't use lists for storage (slow lookups by ID)
- Don't forget to update timestamps
- Don't modify objects returned from storage directly
- Don't reuse deleted IDs (keep incrementing)
- Don't store sensitive data in memory without encryption

## Memory Management
- For large datasets, implement size limits
- Consider cleanup methods for old data
- Be aware of memory usage with many objects
- Use `__slots__` in classes if memory is tight
```