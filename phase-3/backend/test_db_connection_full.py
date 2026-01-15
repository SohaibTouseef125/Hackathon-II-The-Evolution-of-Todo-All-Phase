#!/usr/bin/env python3
"""
Test script to diagnose the database connection issue with full parameters
"""

import os
from dotenv import load_dotenv
from sqlalchemy.pool import QueuePool

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable is not set")
    exit(1)

print(f"Database URL: {DATABASE_URL[:50]}...")  # Print first 50 chars

# Try to create engine with the same parameters as in db.py
try:
    from sqlmodel import create_engine
    print("✓ SQLModel imports successfully")

    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,  # Validates connections before use
        pool_recycle=300,    # Recycle connections after 5 minutes
    )
    print("✓ Engine created successfully with all parameters")

except Exception as e:
    print(f"✗ Failed to create engine: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    exit(1)

print("All tests passed!")