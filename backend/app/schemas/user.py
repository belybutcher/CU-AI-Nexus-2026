"""Pydantic schemas for user representation."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    """Public representation of a user, returned by GET /me."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    created_at: datetime
