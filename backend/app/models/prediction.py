"""Prediction ORM model — stores a single AI inference run (any disease/modality)."""
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.utils.db_types import GUID


class Prediction(Base):
    """
    Result of running a classification model on an (optionally enhanced) image.

    `modality` and `disease` are free-form strings (e.g. "ultrasound"/"breast",
    "xray"/"lung") so new diseases never require a schema migration.
    """

    __tablename__ = "predictions"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("users.id"), nullable=False)
    patient_id: Mapped[uuid.UUID | None] = mapped_column(GUID(), ForeignKey("patients.id"), nullable=True)

    modality: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g. "ultrasound", "xray", "mri"
    disease: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g. "breast", "lung", "skin", "retina"

    original_image_path: Mapped[str] = mapped_column(String(500), nullable=False)
    enhanced_image_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    heatmap_path: Mapped[str | None] = mapped_column(String(500), nullable=True)

    predicted_label: Mapped[str] = mapped_column(String(100), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    class_probabilities: Mapped[dict] = mapped_column(JSON, default=dict)  # {"benign": 0.1, "malignant": 0.85, ...}
    model_version: Mapped[str] = mapped_column(String(50), default="placeholder-v0")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user: Mapped["User"] = relationship(back_populates="predictions")
    patient: Mapped["Patient | None"] = relationship(back_populates="predictions")
    reports: Mapped[list["MedicalReport"]] = relationship(back_populates="prediction", cascade="all, delete-orphan")
