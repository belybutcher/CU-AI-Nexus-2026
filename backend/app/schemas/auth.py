"""Pydantic schemas for authentication endpoints."""
from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    """Payload for POST /register."""

    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)


class UserLoginRequest(BaseModel):
    """Payload for POST /login."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Response returned by /login and /register."""

    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int
