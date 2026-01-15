#!/usr/bin/env python3
"""
Test script to verify that data is saved to the Neon database.
"""

from sqlmodel import create_engine, Session, select
import os
from dotenv import load_dotenv
from models import User, Task
from services.user_service import UserService
import uuid
from datetime import datetime

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

def test_neon_database():
    """Test that data is saved to the Neon database."""
    print("Testing Neon database connection and data persistence...")

    # Count existing users and tasks
    with Session(engine) as session:
        existing_users = session.exec(select(User)).all()
        existing_tasks = session.exec(select(Task)).all()
        print(f"Existing users in database: {len(existing_users)}")
        print(f"Existing tasks in database: {len(existing_tasks)}")

        # Create a new user to test data persistence
        test_email = f"neontest_{uuid.uuid4()}@example.com"
        new_user = User(
            email=test_email,
            name="Neon Test User",
            hashed_password=UserService.get_password_hash("testpassword123"),
            is_active=True,
            created_at=datetime.utcnow()
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        print(f"Created new user: {new_user.email} with ID: {new_user.id}")

        # Create a task for this user
        new_task = Task(
            title="Test Task for Neon DB",
            description="This task verifies Neon database connection",
            completed=False,
            user_id=new_user.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        print(f"Created new task: {new_task.title} with ID: {new_task.id}")

        # Verify the data was saved by querying it back
        saved_user = session.get(User, new_user.id)
        if saved_user:
            print(f"✓ Found user in database: {saved_user.email}")
        else:
            print("✗ ERROR: User not found after saving!")

        saved_task = session.get(Task, new_task.id)
        if saved_task:
            print(f"✓ Found task in database: {saved_task.title}")
        else:
            print("✗ ERROR: Task not found after saving!")

        # Count users and tasks after insertion
        updated_users = session.exec(select(User)).all()
        updated_tasks = session.exec(select(Task)).all()
        print(f"Users after insertion: {len(updated_users)}")
        print(f"Tasks after insertion: {len(updated_tasks)}")

        # Clean up - delete the test records
        session.delete(saved_task)
        session.delete(saved_user)
        session.commit()
        print("Test records cleaned up.")

    print("Neon database test completed successfully!")
    print("✓ Data is being saved to the Neon PostgreSQL database")

if __name__ == "__main__":
    test_neon_database()