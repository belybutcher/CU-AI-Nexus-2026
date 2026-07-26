"""Business logic for viewing and deleting a user's diagnostic history."""
import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenException, NotFoundException
from app.database.repositories.prediction_repository import PredictionRepository
from app.schemas.history import HistoryItem, HistoryListResponse


class HistoryService:
    """Read/delete operations over a user's past predictions."""

    def __init__(self, db: Session):
        self.db = db
        self.prediction_repo = PredictionRepository(db)

    def get_history(self, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> HistoryListResponse:
        """Return the current user's prediction history, most recent first."""
        predictions = self.prediction_repo.list_for_user(user_id, skip=skip, limit=limit)
        items = [
            HistoryItem(
                prediction_id=p.id,
                disease=p.disease,
                modality=p.modality,
                predicted_label=p.predicted_label,
                confidence=p.confidence,
                created_at=p.created_at,
            )
            for p in predictions
        ]
        return HistoryListResponse(items=items, total=len(items))

    def delete_history_item(self, user_id: uuid.UUID, prediction_id: uuid.UUID) -> None:
        """Delete a prediction from history, if it belongs to the requesting user."""
        prediction = self.prediction_repo.get(prediction_id)
        if not prediction:
            raise NotFoundException(f"Prediction '{prediction_id}' not found.")
        if prediction.user_id != user_id:
            raise ForbiddenException("You cannot delete another user's history.")
        self.prediction_repo.delete(prediction)
