"""File-system helpers for saving/validating uploaded and generated files."""
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings
from app.core.exceptions import InvalidFileException


def validate_image_extension(filename: str) -> str:
    """Ensure the uploaded file has an allowed image extension. Returns the lowercase extension."""
    ext = Path(filename).suffix.lower()
    if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
        raise InvalidFileException(
            f"Unsupported file extension '{ext}'. Allowed: {settings.ALLOWED_IMAGE_EXTENSIONS}"
        )
    return ext


async def save_upload_file(upload_file: UploadFile, subfolder: str) -> Path:
    """
    Persist an UploadFile to disk under `app/storage/<subfolder>/<uuid><ext>`.

    Returns the absolute path of the saved file. Enforces the configured
    max upload size while streaming to avoid loading huge files fully into memory.
    """
    ext = validate_image_extension(upload_file.filename or "")
    destination_dir = settings.storage_path(subfolder)
    destination_path = destination_dir / f"{uuid.uuid4()}{ext}"

    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    size = 0
    with open(destination_path, "wb") as out_file:
        while chunk := await upload_file.read(1024 * 1024):
            size += len(chunk)
            if size > max_bytes:
                out_file.close()
                destination_path.unlink(missing_ok=True)
                raise InvalidFileException(
                    f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB."
                )
            out_file.write(chunk)

    await upload_file.close()
    return destination_path


def build_storage_relative_path(absolute_path: Path) -> str:
    """Convert an absolute storage path into a relative path safe to store in the DB."""
    return str(absolute_path.relative_to(settings.STORAGE_ROOT))
