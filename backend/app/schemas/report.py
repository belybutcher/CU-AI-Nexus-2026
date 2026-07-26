"""Pydantic schemas for report generation endpoints."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class GenerateReportRequest(BaseModel):
    """Payload for POST /generate-report."""

    prediction_id: UUID = Field(..., description="Prediction to build the report from")
    file_format: str = Field("pdf", pattern="^(pdf|html)$")


class ReportResponse(BaseModel):
    """Response returned by POST /generate-report and GET /report/{id}."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    prediction_id: UUID
    file_path: str
    file_format: str
    summary: str | None
    created_at: datetime
