"""
Business logic for image upload and enhancement.

Design note: uploaded/enhanced files are stored as `<uuid><ext>` on disk
(see `app/utils/storage_lookup.py`), so this service can resolve an image
purely by id without a dedicated Image table. Once a prediction or report
is generated from an image, its resolved path is persisted permanently on
that record.
"""
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import UploadFile

from app.ai.enhancement import enhancer
from app.core.config import settings
from app.utils.file_utils import build_storage_relative_path, save_upload_file, validate_image_extension
from app.utils.image_utils import open_image, save_image
from app.utils.storage_lookup import find_file_by_id
from app.schemas.image import EnhanceImageResponse, ImageUploadResponse

logger = logging.getLogger(__name__)


class ImageService:
    """Handles saving raw uploads and running the enhancement pipeline."""

    async def upload_image(self, file: UploadFile, disease: str, modality: str) -> ImageUploadResponse:
        """Validate and persist an uploaded medical image."""
        validate_image_extension(file.filename or "")
        saved_path = await save_upload_file(file, settings.UPLOAD_DIR)

        return ImageUploadResponse(
            image_id=uuid.UUID(saved_path.stem),
            original_filename=file.filename or saved_path.name,
            stored_path=build_storage_relative_path(saved_path),
            modality=modality,
            disease=disease,
            uploaded_at=datetime.now(timezone.utc),
        )

    def enhance(self, image_id: uuid.UUID) -> EnhanceImageResponse:
        """Run the AI enhancement pipeline on a previously uploaded image."""
        source_path = find_file_by_id(settings.UPLOAD_DIR, image_id)
        image = open_image(source_path)

        enhanced_image = enhancer.enhance_image(image)

        destination = settings.storage_path(settings.ENHANCED_DIR) / f"{image_id}{source_path.suffix}"
        save_image(enhanced_image, destination)

        return EnhanceImageResponse(
            image_id=image_id,
            enhanced_path=build_storage_relative_path(destination),
            model_version=enhancer.model_version,
            processed_at=datetime.now(timezone.utc),
        )

    def get_enhanced(self, image_id: uuid.UUID) -> EnhanceImageResponse:
        """Retrieve metadata about a previously enhanced image."""
        path = find_file_by_id(settings.ENHANCED_DIR, image_id)
        return EnhanceImageResponse(
            image_id=image_id,
            enhanced_path=build_storage_relative_path(path),
            model_version=enhancer.model_version,
            processed_at=datetime.fromtimestamp(path.stat().st_mtime),
        )
