import pytest
from sqlmodel import Session
from main import app
from fastapi.testclient import TestClient
from db import engine


@pytest.fixture(name="session")
def session_fixture():
    # Use the same Postgres engine as the main application
    from models import SQLModel
    # Note: In a real testing environment, you might want to create a separate test database
    # For now, we're using the same engine as the main application
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture():
    client = TestClient(app)
    yield client