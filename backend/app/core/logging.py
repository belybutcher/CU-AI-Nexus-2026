"""
Centralized logging configuration.

Call `configure_logging()` once at application startup (see app/main.py).
Every module should then just do:

    import logging
    logger = logging.getLogger(__name__)

and logs will inherit the root configuration (format, level, handlers).
"""
import logging
import sys

from app.core.config import settings


class _JsonFormatter(logging.Formatter):
    """Minimal JSON log formatter, useful for log aggregation (ELK, CloudWatch, etc.)."""

    def format(self, record: logging.LogRecord) -> str:
        import json

        payload = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload)


def configure_logging() -> None:
    """Configure the root logger for the whole application."""
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)

    # Avoid duplicate handlers on reload (uvicorn --reload re-imports modules)
    if root_logger.handlers:
        return

    handler = logging.StreamHandler(sys.stdout)
    if settings.LOG_JSON:
        handler.setFormatter(_JsonFormatter())
    else:
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
    root_logger.addHandler(handler)

    # Quiet down noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.DEBUG else logging.WARNING
    )
