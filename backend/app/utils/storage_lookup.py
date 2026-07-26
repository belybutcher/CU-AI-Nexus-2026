"""
Helpers for locating stored files by their UUID identifier.

Design note: uploaded/enhanced images are named `<uuid><ext>` on disk. This
lets any layer resolve a file purely from its id + a known storage
subfolder, without needing a dedicated "Image" database table just to track
filenames. Prediction/report records still persist the resolved path once
they're created, for permanent traceability.
"""
from pathlib import Path
from uuid import UUID

from app.core.config import settings
from app.core.exceptions import NotFoundException


def find_file_by_id(subfolder: str, file_id: UUID) -> Path:
    """Find a file named `<file_id>.*` inside the given storage subfolder."""
    directory = settings.storage_path(subfolder)
    matches = list(directory.glob(f"{file_id}.*"))
    if not matches:
        raise NotFoundException(f"No file found for id '{file_id}' in '{subfolder}'.")
    return matches[0]
