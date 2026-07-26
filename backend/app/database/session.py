"""
SQLAlchemy engine and session management.

Uses SQLite by default (zero-config local development) and switches
transparently to PostgreSQL when DATABASE_URL points to one (production).
"""
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# SQLite needs this connect_arg when used with multiple threads (FastAPI's threadpool).
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,  # gracefully recover from dropped DB connections
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a DB session and guarantees it's closed."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
