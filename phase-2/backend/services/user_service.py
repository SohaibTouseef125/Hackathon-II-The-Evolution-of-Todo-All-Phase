from sqlmodel import Session, select
from typing import Optional
from datetime import datetime
import uuid
from passlib.context import CryptContext

from models import User, UserCreate, UserUpdate


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password"""
        # Truncate password to 72 characters for bcrypt compatibility
        if len(plain_password) > 72:
            plain_password = plain_password[:72]
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password, truncating to 72 characters if needed for bcrypt compatibility"""
        # Bcrypt has a maximum password length of 72 bytes/characters
        # Truncate the password to 72 characters if it's longer
        safe_password = password.encode("utf-8")[:72]
        return pwd_context.hash(safe_password)
        
    


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
