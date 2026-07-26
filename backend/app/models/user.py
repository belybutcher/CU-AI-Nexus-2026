"""User ORM model."""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.utils.db_types import GUID


class User(Base):
    """A registered platform user (doctor, technician, or admin)."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="clinician", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    patients: Mapped[list["Patient"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
    predictions: Mapped[list["Prediction"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    chat_messages: Mapped[list["ChatHistory"]] = relationship(back_populates="user", cascade="all, delete-orphan")
