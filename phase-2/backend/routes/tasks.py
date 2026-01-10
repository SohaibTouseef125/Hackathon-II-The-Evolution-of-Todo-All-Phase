from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from datetime import datetime
import uuid

# Adjust imports for running from backend directory
try:
    from ..models import Task, TaskCreate, TaskRead, TaskUpdate, User
    from ..db import get_session
    from ..auth import get_current_user
    from ..services.task_service import TaskService
except (ImportError, ValueError):
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from models import Task, TaskCreate, TaskRead, TaskUpdate, User
    from db import get_session
    from auth import get_current_user
    from services.task_service import TaskService

from fastapi.security import HTTPAuthorizationCredentials

router = APIRouter()


@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    """Get all tasks for the authenticated user"""
    # Use the current user's ID from the token
    user_id = uuid.UUID(str(current_user.id))

    # Get tasks for the authenticated user using service
    tasks = TaskService.get_tasks_by_user(session, user_id)

    # Convert to response model
    return [
        TaskRead(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        for task in tasks
    ]


@router.post("/tasks", response_model=TaskRead)
def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    """Create a new task for the authenticated user"""
    # Use the current user's ID from the token
    user_id = uuid.UUID(str(current_user.id))

    # Create new task using service
    db_task = TaskService.create_task(session, task, user_id)

    # Convert to response model
    return TaskRead(
        id=db_task.id,
        user_id=db_task.user_id,
        title=db_task.title,
        description=db_task.description,
        completed=db_task.completed,
        created_at=db_task.created_at,
        updated_at=db_task.updated_at
    )


@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(
    task_id: str,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    """Get a specific task by ID"""
    # Use the current user's ID from the token
    user_id = uuid.UUID(str(current_user.id))

    # Get the specific task using service
    task = TaskService.get_task_by_id(session, uuid.UUID(task_id), user_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Convert to response model
    return TaskRead(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    """Update a specific task by ID"""
    # Use the current user's ID from the token
    user_id = uuid.UUID(str(current_user.id))

    # Get the specific task using service
    db_task = TaskService.get_task_by_id(session, uuid.UUID(task_id), user_id)

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update task using service
    updated_task = TaskService.update_task(session, db_task, task_update)

    # Convert to response model
    return TaskRead(
        id=updated_task.id,
        user_id=updated_task.user_id,
        title=updated_task.title,
        description=updated_task.description,
        completed=updated_task.completed,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at
    )


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: str,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    """Delete a specific task by ID"""
    # Use the current user's ID from the token
    user_id = uuid.UUID(str(current_user.id))

    # Get the specific task using service
    db_task = TaskService.get_task_by_id(session, uuid.UUID(task_id), user_id)

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Delete the task using service
    TaskService.delete_task(session, db_task)

    return {"message": "Task deleted successfully"}


@router.patch("/tasks/{task_id}/complete", response_model=TaskRead)
def toggle_task_completion(
    task_id: str,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    """Toggle the completion status of a task"""
    # Use the current user's ID from the token
    user_id = uuid.UUID(str(current_user.id))

    # Get the specific task using service
    db_task = TaskService.get_task_by_id(session, uuid.UUID(task_id), user_id)

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle the completion status using service
    updated_task = TaskService.toggle_task_completion(session, db_task)

    # Convert to response model
    return TaskRead(
        id=updated_task.id,
        user_id=updated_task.user_id,
        title=updated_task.title,
        description=updated_task.description,
        completed=updated_task.completed,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at
    )