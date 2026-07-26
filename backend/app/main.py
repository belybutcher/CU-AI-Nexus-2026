"""
CU AI Nexus backend — application entrypoint.

Wires together configuration, logging, database initialization, middleware,
exception handlers, and the versioned API router. Run locally with:

    uvicorn app.main:app --reload

or via Docker (see Dockerfile / docker-compose.yml).
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
import app.models  # noqa: F401  (registers all models on Base.metadata — see app/models/__init__.py)
from app.database.base import Base
from app.database.session import engine
from app.middleware.cors import add_cors_middleware
from app.middleware.logging_middleware import RequestLoggingMiddleware

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan: startup/shutdown hooks.

    On startup (development only), ensures all tables exist via `create_all()`
    for zero-config local runs. In staging/production, prefer running Alembic
    migrations explicitly (`alembic upgrade head`) — see the `docker-compose.yml`
    `migrate` service and the README — instead of relying on this auto-create step.
    """
    if settings.ENVIRONMENT == "development":
        Base.metadata.create_all(bind=engine)
        logger.info("Development mode: ensured all tables exist via create_all().")
    logger.info(
        "%s started | environment=%s | debug=%s",
        settings.PROJECT_NAME,
        settings.ENVIRONMENT,
        settings.DEBUG,
    )
    yield
    logger.info("%s shutting down.", settings.PROJECT_NAME)


def create_application() -> FastAPI:
    """Application factory: builds and configures the FastAPI instance."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=(
            "Modular backend infrastructure for the CU AI Nexus medical AI platform. "
            "Provides image upload/enhancement, pluggable disease classification, "
            "Grad-CAM explainability, an AI medical assistant, report generation, "
            "and patient/prediction history — all AI inference points are placeholder "
            "interfaces ready for engineers to plug real models into."
        ),
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # --- Middleware ---
    add_cors_middleware(app)
    app.add_middleware(RequestLoggingMiddleware)

    # --- Exception handlers ---
    register_exception_handlers(app)

    # --- Routes ---
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    return app


app = create_application()
