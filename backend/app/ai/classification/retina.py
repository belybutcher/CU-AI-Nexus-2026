"""
Retinal fundus disease classifier — PLACEHOLDER implementation.

Mirrors the reference pattern in `breast.py`. Replace the bodies of
`load_model()`, `preprocess()`, and `predict()` with real model code;
nothing outside this file needs to change. See `app/ai/registry.py` for
how this module gets wired up, and `breast.py` for a fully-annotated example.
"""
import logging
from typing import Any

from PIL import Image

from app.ai.base import ClassificationResult

logger = logging.getLogger(__name__)

disease_key = "retina"
labels = ['no_dr', 'mild_dr', 'moderate_dr', 'severe_dr', 'proliferative_dr']
model_version = "placeholder-v0"

_INPUT_SIZE = (224, 224)
_model_cache: Any = None


def load_model() -> Any:
    """TODO(AI engineer): load real 'retina' model weights here."""
    global _model_cache
    if _model_cache is None:
        logger.info("Loading placeholder model for disease='%s'", disease_key)
        _model_cache = "placeholder-retina-model"
    return _model_cache


def preprocess(image: Image.Image):
    """TODO(AI engineer): real preprocessing for 'retina' images."""
    return image.convert("RGB").resize(_INPUT_SIZE)


def predict(image: Image.Image) -> ClassificationResult:
    """TODO(AI engineer): replace with a real forward pass. See breast.py for the pattern."""
    load_model()
    preprocess(image)

    # Deterministic placeholder: uniform-ish distribution favoring the first label.
    n = len(labels)
    base = round(1 / n, 4)
    class_probabilities = {label: base for label in labels}
    class_probabilities[labels[0]] = round(1 - base * (n - 1), 4)
    predicted_label = max(class_probabilities, key=class_probabilities.get)
    confidence = class_probabilities[predicted_label]

    return ClassificationResult(
        predicted_label=predicted_label,
        confidence=confidence,
        class_probabilities=class_probabilities,
    )
