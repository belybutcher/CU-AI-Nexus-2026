"""Authentication endpoints: register, login, current-user profile."""
import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.auth import TokenResponse, UserLoginRequest, UserRegisterRequest
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=201, summary="Register a new user")
async def register(payload: UserRegisterRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """Create a new user account and return an access token."""
    return AuthService(db).register(payload)


@router.post("/login", response_model=TokenResponse, summary="Authenticate and receive an access token")
async def login(payload: UserLoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """Authenticate with email/password and receive a JWT access token."""
    return AuthService(db).login(payload)


@router.get("/me", response_model=UserResponse, summary="Get the current authenticated user's profile")
async def me(current_user: User = Depends(get_current_user)) -> UserResponse:
    """Return the profile of the currently authenticated user."""
    return UserResponse.model_validate(current_user)
