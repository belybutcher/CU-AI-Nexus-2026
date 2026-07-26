"""Pydantic schemas for the patient/prediction history endpoints."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class HistoryItem(BaseModel):
    """A single row in the user's diagnostic history."""

    model_config = ConfigDict(from_attributes=True)

    prediction_id: UUID
    disease: str
    modality: str
    predicted_label: str
    confidence: float
    created_at: datetime


class HistoryListResponse(BaseModel):
    """Response returned by GET /history."""

    items: list[HistoryItem]
    total: int
