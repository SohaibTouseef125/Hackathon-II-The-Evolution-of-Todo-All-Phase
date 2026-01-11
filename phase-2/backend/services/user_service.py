from sqlmodel import Session, select
from typing import Optional
from datetime import datetime
import uuid
import hashlib
from passlib.context import CryptContext

from models import User, UserCreate, UserUpdate


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    @staticmethod
    def _normalize_password(password: str) -> str:
        """Normalize password using SHA-256 to handle any length password safely."""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password"""
        normalized = UserService._normalize_password(plain_password)
        return pwd_context.verify(normalized, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password using SHA-256 normalization followed by bcrypt"""
        normalized = UserService._normalize_password(password)
        return pwd_context.hash(normalized)

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """Get a user by email"""
        user = session.exec(
            select(User).where(User.email == email)
        ).first()
        return user

    @staticmethod
    def get_user_by_id(session: Session, user_id: uuid.UUID) -> Optional[User]:
        """Get a user by ID"""
        user = session.exec(
            select(User).where(User.id == user_id)
        ).first()
        return user

    @staticmethod
    def create_user(session: Session, user_create: UserCreate) -> User:
        """Create a new user"""
        # Hash the password
        hashed_password = UserService.get_password_hash(user_create.password)

        # Create new user
        db_user = User(
            email=user_create.email,
            name=user_create.name,
            hashed_password=hashed_password
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(session: Session, db_user: User, user_update: UserUpdate) -> User:
        """Update a user with provided fields"""
        for field, value in user_update.dict(exclude_unset=True).items():
            setattr(db_user, field, value)

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(session: Session, db_user: User) -> bool:
        """Delete a user"""
        session.delete(db_user)
        session.commit()
        return True
