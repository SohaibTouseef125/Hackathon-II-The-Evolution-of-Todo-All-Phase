from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: Optional[str] = Field(default=None, max_length=100)

    class Config:
        protected_namespaces = ()


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = False

    class Config:
        protected_namespaces = ()


class ConversationBase(SQLModel):
    pass


class MessageBase(SQLModel):
    role: str = Field(regex="^(user|assistant)$")  # Either user or assistant
    content: str = Field(min_length=1)

    class Config:
        protected_namespaces = ()


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")
    # Relationship to conversations
    conversations: List["Conversation"] = Relationship(back_populates="user")
    # Relationship to messages
    messages: List["Message"] = Relationship()


class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: User = Relationship(back_populates="tasks")


class Conversation(ConversationBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: User = Relationship(back_populates="conversations")
    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")


class Message(MessageBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", nullable=False, index=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    tool_calls: Optional[str] = Field(default=None)  # Store as JSON string

    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
    user: User = Relationship()


class UserCreate(UserBase):
    email: str
    password: str = Field(min_length=8)  # No max_length - handled by SHA-256 normalization


class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class MessageCreate(MessageBase):
    conversation_id: uuid.UUID
    user_id: uuid.UUID


class MessageRead(MessageBase):
    id: uuid.UUID
    conversation_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    tool_calls: Optional[str] = None