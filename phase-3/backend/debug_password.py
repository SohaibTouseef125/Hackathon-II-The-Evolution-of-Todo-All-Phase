from sqlmodel import SQLModel, Field, Session, create_engine, select
from passlib.context import CryptContext
from typing import Optional
import uuid
from datetime import datetime

# Define minimal User model for testing
class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

# Create in-memory database for testing
engine = create_engine("sqlite:///:memory:", echo=True)
SQLModel.metadata.create_all(engine)

# Test password hashing and verification
plain_password = "securepassword"
hashed = get_password_hash(plain_password)
print(f"Plain password: {plain_password}")
print(f"Hashed password: {hashed}")
print(f"Verification result: {verify_password(plain_password, hashed)}")
print(f"Wrong password verification: {verify_password('wrongpassword', hashed)}")

# Test creating and retrieving user
with Session(engine) as session:
    # Create user
    new_user = User(
        email="test@example.com",
        name="Test User",
        hashed_password=hashed
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    print(f"\nCreated user: {new_user.email}, {new_user.id}")

    # Retrieve user and verify password
    user = session.exec(select(User).where(User.email == "test@example.com")).first()
    if user:
        print(f"Retrieved user: {user.email}")
        print(f"Stored hash: {user.hashed_password}")
        print(f"Password verification: {verify_password(plain_password, user.hashed_password)}")
        print(f"Wrong password verification: {verify_password('wrongpassword', user.hashed_password)}")
    else:
        print("User not found!")