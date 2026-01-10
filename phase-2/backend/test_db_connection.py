#!/usr/bin/env python3
"""
Test script to diagnose the database connection issue
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable is not set")
    exit(1)

print(f"Database URL: {DATABASE_URL[:50]}...")  # Print first 50 chars

# Check if it's a Postgres URL
if not DATABASE_URL.startswith("postgresql://"):
    print("ERROR: DATABASE_URL is not a PostgreSQL URL")
    exit(1)

# Try to test the import without creating an engine
try:
    from sqlmodel import Session
    print("✓ SQLModel imports successfully")
except ImportError as e:
    print(f"✗ Failed to import SQLModel: {e}")
    exit(1)

try:
    from sqlalchemy import create_engine
    print("✓ SQLAlchemy imports successfully")
except ImportError as e:
    print(f"✗ Failed to import SQLAlchemy create_engine: {e}")
    exit(1)

# Try to parse the URL to check if it's valid
try:
    import urllib.parse
    parsed = urllib.parse.urlparse(DATABASE_URL)
    print(f"✓ URL parses correctly: {parsed.scheme}://{parsed.hostname}")
except Exception as e:
    print(f"✗ Failed to parse URL: {e}")
    exit(1)

# Try to create engine (this is where the error occurs)
try:
    engine = create_engine(DATABASE_URL)
    print("✓ Engine created successfully")
except Exception as e:
    print(f"✗ Failed to create engine: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    exit(1)

print("All tests passed!")