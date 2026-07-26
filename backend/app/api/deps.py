"""
Shared FastAPI dependencies: DB session access and current-user resolution.

Centralizing dependency injection here keeps route handlers thin and makes
auth logic testable/mockable in one place.
"""
from typing import Generator
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.exceptions import UnauthorizedException
from app.core.security import decode_access_token
from app.database.repositories.user_repository import UserRepository
from app.database.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login", auto_error=False)


def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Resolve the authenticated user from the Bearer JWT, or raise 401."""
    if not token:
        raise UnauthorizedException("Missing bearer token.")

    try:
        payload = decode_access_token(token)
    except JWTError:
        raise UnauthorizedException("Invalid or expired token.")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Token missing subject claim.")

    user = UserRepository(db).get(UUID(user_id))
    if not user or not user.is_active:
        raise UnauthorizedException("User not found or inactive.")

    return user
