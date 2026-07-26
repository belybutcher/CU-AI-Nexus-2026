"""Patient ORM model — represents the medical record subject, not the platform user."""
import uuid
from datetime import date, datetime, timezone

from sqlalchemy import DateTime, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.utils.db_types import GUID


class Patient(Base):
    """A patient whose medical images/history are tracked in the system."""

    __tablename__ = "patients"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("users.id"), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    sex: Mapped[str | None] = mapped_column(String(20), nullable=True)
    medical_record_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    owner: Mapped["User"] = relationship(back_populates="patients")
    predictions: Mapped[list["Prediction"]] = relationship(back_populates="patient", cascade="all, delete-orphan")
