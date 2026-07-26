"""
Abstract base interfaces for all AI components.

These are the contracts that AI engineers implement. The API and service
layers only ever talk to these interfaces — never to a specific model's
implementation details — so swapping PyTorch for ONNX, or adding a brand new
disease, never requires touching `app/api` or `app/services`.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from PIL import Image


class BaseClassifier(ABC):
    """
    Contract every disease-classification module must implement.

    A concrete module (e.g. `app/ai/classification/breast.py`) exposes a
    module-level instance of a subclass of this, or plain module-level
    functions matching these signatures — see breast.py for the reference
    implementation and README for both patterns.
    """

    #: Unique key used to look this classifier up in the registry, e.g. "breast".
    disease_key: str = "base"
    #: Human-readable class labels this model predicts, in output order.
    labels: list[str] = []
    #: Free-text version identifier, surfaced in API responses for traceability.
    model_version: str = "unversioned"

    @abstractmethod
    def load_model(self) -> Any:
        """
        Load (and cache) the underlying model weights/architecture.

        Should be idempotent and safe to call multiple times (e.g. lazy-load
        on first use, then return the cached instance).
        """
        raise NotImplementedError

    @abstractmethod
    def preprocess(self, image: Image.Image) -> Any:
        """Turn a PIL image into whatever tensor/array format the model expects."""
        raise NotImplementedError

    @abstractmethod
    def predict(self, image: Image.Image) -> "ClassificationResult":
        """Run the full pipeline (preprocess + forward pass) and return a structured result."""
        raise NotImplementedError


class ClassificationResult:
    """Standard structured output every classifier must return from `predict()`."""

    def __init__(self, predicted_label: str, confidence: float, class_probabilities: dict[str, float]):
        self.predicted_label = predicted_label
        self.confidence = confidence
        self.class_probabilities = class_probabilities

    def to_dict(self) -> dict:
        return {
            "predicted_label": self.predicted_label,
            "confidence": self.confidence,
            "class_probabilities": self.class_probabilities,
        }


class BaseEnhancer(ABC):
    """Contract for image-quality-enhancement modules (e.g. denoising, super-resolution GANs)."""

    model_version: str = "unversioned"

    @abstractmethod
    def load_model(self) -> Any:
        """Load (and cache) the enhancement model."""
        raise NotImplementedError

    @abstractmethod
    def enhance_image(self, image: Image.Image) -> Image.Image:
        """Return an enhanced copy of the input image."""
        raise NotImplementedError


class BaseGradCAM(ABC):
    """Contract for Grad-CAM (or similar explainability) heatmap generators."""

    @abstractmethod
    def generate_heatmap(self, image: Image.Image, disease_key: str) -> Image.Image:
        """
        Produce a heatmap overlay highlighting the regions that most influenced
        the classifier's decision for the given disease model.
        """
        raise NotImplementedError
