"""Pydantic schemas for image upload & enhancement endpoints."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ImageUploadResponse(BaseModel):
    """Response returned by POST /upload."""

    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

    image_id: UUID = Field(..., description="Identifier to reference this image in later calls")
    original_filename: str
    stored_path: str
    modality: str
    disease: str
    uploaded_at: datetime


class EnhanceImageRequest(BaseModel):
    """Payload for POST /enhance."""

    image_id: UUID = Field(..., description="ID returned by POST /upload")
    disease: str = Field(..., description="Disease/modality key, e.g. 'breast', 'lung'")


class EnhanceImageResponse(BaseModel):
    """Response returned by POST /enhance and GET /enhanced/{id}."""

    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

    image_id: UUID
    enhanced_path: str
    model_version: str
    processed_at: datetime
