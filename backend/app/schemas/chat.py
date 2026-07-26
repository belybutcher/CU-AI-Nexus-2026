"""Pydantic schemas for the chatbot endpoint."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    """Payload for POST /chat."""

    question: str = Field(..., min_length=1, max_length=2000)
    prediction_id: Optional[UUID] = Field(
        None, description="Optional prediction to ground the answer in (adds it to RAG context)"
    )


class ChatResponse(BaseModel):
    """Response returned by POST /chat."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    question: str
    answer: str
    retrieved_context: list[str]
    created_at: datetime
