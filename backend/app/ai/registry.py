"""
Disease classifier registry — the single mechanism that makes the AI layer modular.

To add support for a brand-new disease, an AI engineer:
  1. Creates `app/ai/classification/<disease>.py` implementing `load_model()`,
     `preprocess()`, and `predict()` (see `breast.py` for the reference shape).
  2. Registers it below with one line.

Nothing in `app/api` or `app/services` needs to change.
"""
import logging
from typing import Callable

from app.core.exceptions import ModelNotAvailableException

logger = logging.getLogger(__name__)

# Maps disease_key -> module import path exposing predict()/load_model()/preprocess().
# Lazy-imported on first use so an unimplemented/broken model doesn't crash app startup.
_REGISTRY: dict[str, str] = {
    "breast": "app.ai.classification.breast",
    "lung": "app.ai.classification.lung",
    "skin": "app.ai.classification.skin",
    "retina": "app.ai.classification.retina",
}

_module_cache: dict[str, object] = {}


def register_classifier(disease_key: str, module_path: str) -> None:
    """Register (or override) a disease classifier module at runtime."""
    _REGISTRY[disease_key] = module_path
    _module_cache.pop(disease_key, None)
    logger.info("Registered classifier '%s' -> %s", disease_key, module_path)


def list_supported_diseases() -> list[str]:
    """Return all disease keys currently registered."""
    return sorted(_REGISTRY.keys())


def get_classifier_module(disease_key: str):
    """
    Resolve and return the classifier module for a disease key.

    Raises:
        ModelNotAvailableException: if the disease key is unknown or the module fails to import.
    """
    import importlib

    if disease_key not in _REGISTRY:
        raise ModelNotAvailableException(
            f"No classifier registered for disease '{disease_key}'. "
            f"Supported: {list_supported_diseases()}"
        )

    if disease_key in _module_cache:
        return _module_cache[disease_key]

    try:
        module = importlib.import_module(_REGISTRY[disease_key])
    except Exception as exc:  # broad: any import-time failure in a model plugin
        logger.exception("Failed to import classifier module for '%s'", disease_key)
        raise ModelNotAvailableException(
            f"Classifier for '{disease_key}' failed to load: {exc}"
        ) from exc

    _module_cache[disease_key] = module
    return module
