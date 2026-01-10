from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
import uuid

# Adjust imports for running from backend directory
try:
    from ..models import Task, TaskCreate, TaskUpdate, User
except (ImportError, ValueError):
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from models import Task, TaskCreate, TaskUpdate, User


class TaskService:
    @staticmethod
    def get_tasks_by_user(session: Session, user_id: uuid.UUID) -> List[Task]:
        """Get all tasks for a specific user"""
        tasks = session.exec(
            select(Task).where(Task.user_id == user_id)
        ).all()
        return tasks

    @staticmethod
    def get_task_by_id(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
        """Get a specific task by ID for a specific user"""
        task = session.exec(
            select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id
            )
        ).first()
        return task

    @staticmethod
    def create_task(session: Session, task_create: TaskCreate, user_id: uuid.UUID) -> Task:
        """Create a new task for a user"""
        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            user_id=user_id
        )

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    def update_task(session: Session, db_task: Task, task_update: TaskUpdate) -> Task:
        """Update a task with provided fields"""
        for field, value in task_update.dict(exclude_unset=True).items():
            setattr(db_task, field, value)

        # Update the timestamp
        db_task.updated_at = datetime.utcnow()

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(session: Session, db_task: Task) -> bool:
        """Delete a task"""
        session.delete(db_task)
        session.commit()
        return True

    @staticmethod
    def toggle_task_completion(session: Session, db_task: Task) -> Task:
        """Toggle the completion status of a task"""
        db_task.completed = not db_task.completed
        db_task.updated_at = datetime.utcnow()

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task