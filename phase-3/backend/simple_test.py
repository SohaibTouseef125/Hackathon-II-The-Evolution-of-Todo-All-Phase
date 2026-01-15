from fastapi import FastAPI
from fastapi.testclient import TestClient
from routes.auth import router as auth_router
import pytest
from unittest.mock import patch
from db import get_session
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

# Create app
app = FastAPI(title="Todo API", version="1.0.0")
app.include_router(auth_router, prefix="/api")

# Create test client with in-memory database
def get_test_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session
client = TestClient(app)

# Test registration
print("Testing registration...")
response = client.post("/api/auth/register", json={
    "email": "test@example.com",
    "name": "Test User",
    "password": "securepassword"
})
print(f"Registration status: {response.status_code}")
if response.status_code != 200:
    print(f"Registration error: {response.text}")
else:
    print(f"Registration data: {response.json()}")

# Test login
print("\nTesting login...")
response = client.post("/api/auth/login", data={
    "username": "test@example.com",  # OAuth2PasswordRequestForm expects 'username'
    "password": "securepassword"
})
print(f"Login status: {response.status_code}")
if response.status_code != 200:
    print(f"Login error: {response.text}")
else:
    print(f"Login data: {response.json()}")