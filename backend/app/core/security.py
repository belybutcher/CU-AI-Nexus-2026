"""
Security utilities: password hashing and JWT access-token management.

Kept isolated from the rest of the app so the hashing scheme or token
strategy can be swapped without touching business logic.
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings

# Using the `bcrypt` library directly (rather than passlib's CryptContext)
# avoids a known incompatibility between passlib 1.7.x and bcrypt>=4.1,
# where passlib misreads the backend version and mishandles password length.
_BCRYPT_ROUNDS = 12


def hash_password(password: str) -> str:
    """Hash a plaintext password for storage."""
    salt = bcrypt.gensalt(rounds=_BCRYPT_ROUNDS)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a plaintext password against its stored hash."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None, extra_claims: Optional[dict[str, Any]] = None) -> str:
    """
    Create a signed JWT access token.

    Args:
        subject: Typically the user's UUID (stored in the `sub` claim).
        expires_delta: Optional custom expiry; defaults to settings value.
        extra_claims: Optional additional claims (e.g. role).
    """
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode: dict[str, Any] = {"sub": subject, "exp": expire, "type": "access"}
    if extra_claims:
        to_encode.update(extra_claims)
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT access token.

    Raises:
        JWTError: if the token is invalid, malformed, or expired.
    """
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError as exc:
        raise exc
