from sqlmodel import create_engine, Session
from sqlalchemy import event
from sqlalchemy.pool import QueuePool
import os
from typing import Generator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment - require Postgres URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required for Postgres connection")

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Validates connections before use
    pool_recycle=300,    # Recycle connections after 5 minutes
)

def create_db_and_tables():
    """Create database tables - only for development/testing"""
    from models import User, Task, Conversation, Message
    from sqlmodel import SQLModel

    # Create tables
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Get database session for dependency injection"""
    with Session(engine) as session:
        yield session


# Optional: Add connection event listeners for debugging
@event.listens_for(engine, "connect")
def set_connection_options(dbapi_connection, connection_record):
    """Set database-specific options on connection"""
    # This can be used to set Postgres-specific options if needed
    pass