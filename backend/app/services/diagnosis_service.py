"""
Business logic for running disease classification (+ optional Grad-CAM).

Orchestrates: resolve image -> pick classifier via registry -> predict ->
optionally generate heatmap -> persist a Prediction record.
"""
import logging
import uuid
from pathlib import Path

from sqlalchemy.orm import Session

from app.ai.gradcam import gradcam
from app.ai.registry import get_classifier_module
from app.core.config import settings
from app.core.exceptions import NotFoundException
from app.database.repositories.prediction_repository import PredictionRepository
from app.models.prediction import Prediction
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.utils.file_utils import build_storage_relative_path
from app.utils.image_utils import open_image, save_image
from app.utils.storage_lookup import find_file_by_id

logger = logging.getLogger(__name__)

# Maps disease_key -> modality label. Extend this alongside app/ai/registry.py
# whenever a new disease/modality combination is added.
_MODALITY_BY_DISEASE = {
    "breast": "ultrasound",
    "lung": "xray",
    "skin": "dermatoscopy",
    "retina": "fundus_photography",
}


class DiagnosisService:
    """Runs the classification (and Grad-CAM) pipeline and persists results."""

    def __init__(self, db: Session):
        self.db = db
        self.prediction_repo = PredictionRepository(db)

    def predict(self, user_id: uuid.UUID, payload: PredictionRequest) -> PredictionResponse:
        """Execute the full diagnosis pipeline for a given image + disease."""
        # Prefer an enhanced image if one exists, otherwise fall back to the original upload.
        try:
            image_path = find_file_by_id(settings.ENHANCED_DIR, payload.image_id)
        except NotFoundException:
            image_path = find_file_by_id(settings.UPLOAD_DIR, payload.image_id)

        image = open_image(image_path)

        classifier_module = get_classifier_module(payload.disease)
        result = classifier_module.predict(image)

        heatmap_relative_path = None
        if payload.generate_heatmap:
            heatmap_image = gradcam.generate_heatmap(image, payload.disease)
            heatmap_dest = settings.storage_path(settings.HEATMAP_DIR) / f"{uuid.uuid4()}{image_path.suffix}"
            save_image(heatmap_image, heatmap_dest)
            heatmap_relative_path = build_storage_relative_path(heatmap_dest)

        prediction = Prediction(
            user_id=user_id,
            patient_id=payload.patient_id,
            modality=_MODALITY_BY_DISEASE.get(payload.disease, "unknown"),
            disease=payload.disease,
            original_image_path=build_storage_relative_path(image_path),
            heatmap_path=heatmap_relative_path,
            predicted_label=result.predicted_label,
            confidence=result.confidence,
            class_probabilities=result.class_probabilities,
            model_version=getattr(classifier_module, "model_version", "unversioned"),
        )
        self.prediction_repo.create(prediction)

        return self._to_response(prediction)

    def get_prediction(self, prediction_id: uuid.UUID) -> PredictionResponse:
        """Fetch a previously stored prediction by id."""
        prediction = self.prediction_repo.get(prediction_id)
        if not prediction:
            raise NotFoundException(f"Prediction '{prediction_id}' not found.")
        return self._to_response(prediction)

    @staticmethod
    def _to_response(prediction: Prediction) -> PredictionResponse:
        return PredictionResponse(
            id=prediction.id,
            disease=prediction.disease,
            modality=prediction.modality,
            predicted_label=prediction.predicted_label,
            confidence=prediction.confidence,
            class_probabilities=prediction.class_probabilities,
            heatmap_path=prediction.heatmap_path,
            model_version=prediction.model_version,
            created_at=prediction.created_at,
        )
