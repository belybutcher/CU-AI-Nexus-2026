"""
Centralized application configuration.

All environment-driven settings live here. Values are loaded from a `.env`
file at the project root (see `.env.example`) and validated by Pydantic at
startup, so misconfiguration fails fast instead of surfacing as a runtime
bug deep inside a request handler.
"""
from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # backend/


class Settings(BaseSettings):
    """Application-wide settings, sourced from environment variables."""

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # --- General ---
    PROJECT_NAME: str = "CU AI Nexus"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"  # development | staging | production
    DEBUG: bool = True

    # --- Security / JWT ---
    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24h
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7d

    # --- Database ---
    # Defaults to a local SQLite file so the project runs with zero setup.
    # Point DATABASE_URL at Postgres in staging/production, e.g.:
    # postgresql+psycopg2://user:password@localhost:5432/cu_ai_nexus
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/cu_ai_nexus.db"

    # --- CORS ---
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    # --- Storage ---
    STORAGE_ROOT: Path = BASE_DIR / "app" / "storage"
    UPLOAD_DIR: str = "uploads"
    ENHANCED_DIR: str = "enhanced"
    HEATMAP_DIR: str = "heatmaps"
    REPORT_DIR: str = "reports"
    MAX_UPLOAD_SIZE_MB: int = 25
    ALLOWED_IMAGE_EXTENSIONS: List[str] = [".png", ".jpg", ".jpeg", ".dcm", ".bmp", ".tiff"]

    # --- AI model weights root (mounted volume in Docker) ---
    MODEL_WEIGHTS_DIR: Path = BASE_DIR / "models"

    # --- Logging ---
    LOG_LEVEL: str = "INFO"
    LOG_JSON: bool = False

    # --- Chatbot / RAG placeholder ---
    CHATBOT_KNOWLEDGE_BASE_DIR: Path = BASE_DIR / "app" / "ai" / "chatbot" / "knowledge_base"

    def storage_path(self, subfolder: str) -> Path:
        """Return the absolute path for a given storage subfolder, creating it if needed."""
        path = self.STORAGE_ROOT / subfolder
        path.mkdir(parents=True, exist_ok=True)
        return path


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (loaded once per process)."""
    return Settings()


settings = get_settings()
