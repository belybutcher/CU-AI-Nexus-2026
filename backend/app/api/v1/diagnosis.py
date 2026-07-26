"""Diagnosis / disease-classification endpoints."""
import logging
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.diagnosis_service import DiagnosisService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Diagnosis"])


@router.post("/predict", response_model=PredictionResponse, status_code=201, summary="Run disease classification")
async def predict(
    payload: PredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PredictionResponse:
    """
    Classify a previously uploaded (optionally enhanced) image for the given disease.

    Optionally generates a Grad-CAM heatmap alongside the classification result.
    """
    return DiagnosisService(db).predict(current_user.id, payload)


@router.get("/prediction/{prediction_id}", response_model=PredictionResponse, summary="Fetch a stored prediction")
async def get_prediction(
    prediction_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PredictionResponse:
    """Retrieve a previously generated prediction by id."""
    return DiagnosisService(db).get_prediction(prediction_id)
