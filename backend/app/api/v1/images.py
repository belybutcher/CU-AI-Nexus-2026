"""Image upload & enhancement endpoints."""
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.ai.registry import list_supported_diseases
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.image import EnhanceImageRequest, EnhanceImageResponse, ImageUploadResponse
from app.services.image_service import ImageService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Images"])


@router.post("/upload", response_model=ImageUploadResponse, status_code=201, summary="Upload a medical image")
async def upload_image(
    file: UploadFile = File(..., description="The medical image file"),
    disease: str = Form(..., description=f"Target disease key, one of: {list_supported_diseases()}"),
    modality: str = Form("unspecified", description="Imaging modality, e.g. ultrasound, xray, mri"),
    current_user: User = Depends(get_current_user),
) -> ImageUploadResponse:
    """
    Upload a raw medical image for later enhancement/classification.

    The returned `image_id` is used in subsequent calls to `/enhance` and `/predict`.
    """
    return await ImageService().upload_image(file, disease=disease, modality=modality)


@router.post("/enhance", response_model=EnhanceImageResponse, summary="Enhance a previously uploaded image")
async def enhance_image(
    payload: EnhanceImageRequest,
    current_user: User = Depends(get_current_user),
) -> EnhanceImageResponse:
    """Run the AI image-enhancement pipeline on a previously uploaded image."""
    return ImageService().enhance(payload.image_id)


@router.get("/enhanced/{image_id}", response_model=EnhanceImageResponse, summary="Fetch enhancement metadata")
async def get_enhanced_image(
    image_id: UUID,
    current_user: User = Depends(get_current_user),
) -> EnhanceImageResponse:
    """Retrieve metadata about a previously enhanced image."""
    return ImageService().get_enhanced(image_id)
