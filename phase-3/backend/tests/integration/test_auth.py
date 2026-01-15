import pytest
from fastapi.testclient import TestClient
from main import app
from db import get_session, engine
from models import User, Task
from sqlmodel import Session, SQLModel
from unittest.mock import patch
import uuid


@pytest.fixture(name="client")
def client_fixture():
    def get_test_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_register_user(client: TestClient):
    """Test user registration endpoint"""
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "name": "Test User",
        "password": "securepassword"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert "id" in data


def test_login_user(client: TestClient):
    """Test user login endpoint"""
    # First register a user
    register_response = client.post("/api/auth/register", json={
        "email": "login@example.com",
        "name": "Login User",
        "password": "securepassword"
    })
    assert register_response.status_code == 200

    # Then try to login
    response = client.post("/api/auth/login", data={
        "email": "login@example.com",
        "password": "securepassword"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["email"] == "login@example.com"


def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials"""
    response = client.post("/api/auth/login", data={
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 401


if __name__ == "__main__":
    # Run the tests if this file is executed directly
    import sys
    from fastapi.testclient import TestClient

    # Create a test client
    client = TestClient(app)

    print("Running auth integration tests...")

    # These tests would need a proper test setup to run correctly
    # For now, we'll just print that they're defined
    print("✓ test_register_user defined")
    print("✓ test_login_user defined")
    print("✓ test_login_invalid_credentials defined")
    print("All auth integration tests defined!")