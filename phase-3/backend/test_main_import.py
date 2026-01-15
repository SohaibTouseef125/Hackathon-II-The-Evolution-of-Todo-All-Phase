#!/usr/bin/env python3
"""
Simple test to import main.py directly
"""

print("Attempting to import main.py...")

try:
    import sys
    import os
    # Add the backend directory to the path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    # Import main
    from main import app
    print("✓ Successfully imported main.py")

    # Try to create a test client to see if routes work
    from fastapi.testclient import TestClient
    client = TestClient(app)
    print("✓ Successfully created test client")

    # Test the root endpoint
    response = client.get("/")
    print(f"✓ Root endpoint response: {response.json()}")
    print(f"Status code: {response.status_code}")

except Exception as e:
    print(f"✗ Error importing main.py: {e}")
    import traceback
    traceback.print_exc()