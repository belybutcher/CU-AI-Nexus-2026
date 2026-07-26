"""
Application-wide custom exceptions and their FastAPI exception handlers.

Services and repositories raise these domain-specific exceptions instead of
raising HTTPException directly. This keeps the service layer transport-agnostic
(it doesn't know about HTTP status codes) while the API layer / global handlers
translate them into proper HTTP responses.
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse


class AppException(Exception):
    """Base class for all domain exceptions raised by the application."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message: str = "An unexpected error occurred."

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)


class NotFoundException(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    default_message = "Resource not found."


class AlreadyExistsException(AppException):
    status_code = status.HTTP_409_CONFLICT
    default_message = "Resource already exists."


class InvalidCredentialsException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_message = "Invalid credentials."


class UnauthorizedException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_message = "Not authenticated."


class ForbiddenException(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    default_message = "You do not have permission to perform this action."


class InvalidFileException(AppException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_message = "Uploaded file is invalid or unsupported."


class ModelNotAvailableException(AppException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_message = "The requested AI model is not available yet."


class InferenceException(AppException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = "AI inference failed."


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Translate any AppException subclass into a consistent JSON error response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.__class__.__name__, "detail": exc.message},
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all safety net so raw stack traces never leak to clients."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "InternalServerError", "detail": "Something went wrong. Please try again later."},
    )


def register_exception_handlers(app) -> None:
    """Attach all custom exception handlers to the FastAPI app instance."""
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
