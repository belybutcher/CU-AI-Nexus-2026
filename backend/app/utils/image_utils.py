"""
Lightweight image helper utilities shared across AI modules.

These are intentionally framework-agnostic (no torch/tensorflow import) so
the `utils` layer stays a light dependency for any AI engineer's model code.
"""
from pathlib import Path
from typing import Tuple

from PIL import Image


def open_image(path: str | Path) -> Image.Image:
    """Open an image file and convert to RGB, raising a clear error if unreadable."""
    return Image.open(path).convert("RGB")


def resize_image(image: Image.Image, size: Tuple[int, int]) -> Image.Image:
    """Resize an image to the given (width, height), suitable for model input."""
    return image.resize(size)


def save_image(image: Image.Image, destination: str | Path) -> Path:
    """Save a PIL image to disk, creating parent directories if needed."""
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination)
    return destination
