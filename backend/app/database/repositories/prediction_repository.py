"""Repository for Prediction persistence and lookups."""
from uuid import UUID

from sqlalchemy.orm import Session

from app.database.repositories.base_repository import BaseRepository
from app.models.prediction import Prediction


class PredictionRepository(BaseRepository[Prediction]):
    def __init__(self, db: Session):
        super().__init__(Prediction, db)

    def list_for_user(self, user_id: UUID, skip: int = 0, limit: int = 100) -> list[Prediction]:
        return (
            self.db.query(Prediction)
            .filter(Prediction.user_id == user_id)
            .order_by(Prediction.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
