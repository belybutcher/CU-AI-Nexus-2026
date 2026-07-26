"""Pydantic schemas for diagnosis/prediction endpoints."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PredictionRequest(BaseModel):
    """Payload for POST /predict."""

    image_id: UUID = Field(..., description="ID returned by POST /upload (or the enhanced image id)")
    disease: str = Field(..., description="Which disease/modality model to run, e.g. 'breast', 'lung', 'skin', 'retina'")
    patient_id: Optional[UUID] = Field(None, description="Optional patient to associate this prediction with")
    generate_heatmap: bool = Field(True, description="Whether to also generate a Grad-CAM heatmap")


class PredictionResponse(BaseModel):
    """Response returned by POST /predict and GET /prediction/{id}."""

    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

    id: UUID
    disease: str
    modality: str
    predicted_label: str
    confidence: float
    class_probabilities: dict[str, float]
    heatmap_path: Optional[str] = None
    model_version: str
    created_at: datetime
