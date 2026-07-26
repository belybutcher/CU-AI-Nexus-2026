"""Shared pytest fixtures: an isolated in-memory DB and a TestClient per test."""
import os

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("ENVIRONMENT", "development")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.base import Base
from app.database.session import get_db
from app.main import app


@pytest.fixture()
def db_session():
    """Provide a fresh in-memory SQLite database for each test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    """Provide a FastAPI TestClient wired to the isolated test database."""

    def _get_db_override():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_db_override
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def auth_headers(client):
    """Register a test user and return Authorization headers with a valid access token."""
    response = client.post(
        "/api/v1/register",
        json={"email": "doctor@example.com", "full_name": "Dr. Test", "password": "supersecret123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
