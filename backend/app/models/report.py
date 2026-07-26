"""MedicalReport ORM model — a generated, downloadable report tied to a prediction."""
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.utils.db_types import GUID


class MedicalReport(Base):
    """A generated report (PDF/HTML) summarizing a prediction for a patient."""

    __tablename__ = "medical_reports"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("users.id"), nullable=False)
    prediction_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("predictions.id"), nullable=False)

    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_format: Mapped[str] = mapped_column(String(10), default="pdf")
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    prediction: Mapped["Prediction"] = relationship(back_populates="reports")
