"""Business logic for registration, login, and current-user retrieval."""
from sqlalchemy.orm import Session

from app.core.exceptions import AlreadyExistsException, InvalidCredentialsException
from app.core.security import create_access_token, hash_password, verify_password
from app.database.repositories.user_repository import UserRepository
from app.models.user import User
from app.schemas.auth import TokenResponse, UserLoginRequest, UserRegisterRequest
from app.core.config import settings


class AuthService:
    """Encapsulates authentication use-cases; depends only on the repository layer."""

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register(self, payload: UserRegisterRequest) -> TokenResponse:
        """Create a new user account and return an access token."""
        if self.user_repo.get_by_email(payload.email):
            raise AlreadyExistsException(f"A user with email '{payload.email}' already exists.")

        user = User(
            email=payload.email,
            full_name=payload.full_name,
            hashed_password=hash_password(payload.password),
        )
        self.user_repo.create(user)
        return self._issue_token(user)

    def login(self, payload: UserLoginRequest) -> TokenResponse:
        """Authenticate a user by email/password and return an access token."""
        user = self.user_repo.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.hashed_password):
            raise InvalidCredentialsException("Incorrect email or password.")
        return self._issue_token(user)

    def _issue_token(self, user: User) -> TokenResponse:
        token = create_access_token(subject=str(user.id), extra_claims={"role": user.role})
        return TokenResponse(access_token=token, expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
