"""
Breast ultrasound disease classifier — PLACEHOLDER implementation.

This is the reference module every new disease file should mirror. It
exposes three module-level functions with fixed signatures:

    load_model()   -> loads/caches and returns the model object
    preprocess()   -> PIL.Image -> model-ready tensor/array
    predict()      -> PIL.Image -> ClassificationResult

An AI engineer replaces the body of these three functions with real model
code (e.g. loading a PyTorch checkpoint trained on the BUSI dataset) without
touching anything outside this file. `disease_key`, `labels`, and
`model_version` are read by the registry/service layer for bookkeeping.
"""
import logging
from typing import Any

from PIL import Image

from app.ai.base import ClassificationResult
from app.core.config import settings

logger = logging.getLogger(__name__)

disease_key = "breast"
labels = ["normal", "benign", "malignant"]
model_version = "placeholder-v0"

_INPUT_SIZE = (224, 224)
_model_cache: Any = None


def load_model() -> Any:
    """
    Load (and cache) the breast-ultrasound classification model.

    TODO(AI engineer): replace with real weight loading, e.g.:
        import torch
        model = torch.load(settings.MODEL_WEIGHTS_DIR / "breast_classifier.pt")
        model.eval()
        return model
    """
    global _model_cache
    if _model_cache is None:
        logger.info("Loading placeholder model for disease='%s'", disease_key)
        _model_cache = "placeholder-breast-model"  # sentinel, replace with real model object
    return _model_cache


def preprocess(image: Image.Image):
    """
    Convert a PIL image into the tensor/array format the real model expects.

    TODO(AI engineer): replace with real preprocessing, e.g. resizing,
    normalization to ImageNet stats, and conversion to a torch.Tensor.
    """
    resized = image.convert("RGB").resize(_INPUT_SIZE)
    return resized  # placeholder: return the resized PIL image itself


def predict(image: Image.Image) -> ClassificationResult:
    """
    Run the full breast-ultrasound classification pipeline.

    TODO(AI engineer): replace the body below with:
        model = load_model()
        tensor = preprocess(image)
        with torch.no_grad():
            logits = model(tensor.unsqueeze(0))
            probs = torch.softmax(logits, dim=1).squeeze().tolist()
        class_probabilities = dict(zip(labels, probs))
        predicted_label = max(class_probabilities, key=class_probabilities.get)
        confidence = class_probabilities[predicted_label]
        return ClassificationResult(predicted_label, confidence, class_probabilities)
    """
    load_model()
    preprocess(image)

    # --- Deterministic placeholder output (NOT a real prediction) ---
    class_probabilities = {"normal": 0.10, "benign": 0.25, "malignant": 0.65}
    predicted_label = max(class_probabilities, key=class_probabilities.get)
    confidence = class_probabilities[predicted_label]

    return ClassificationResult(
        predicted_label=predicted_label,
        confidence=confidence,
        class_probabilities=class_probabilities,
    )
