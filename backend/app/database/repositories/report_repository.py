"""Repository for MedicalReport persistence and lookups."""
from uuid import UUID

from sqlalchemy.orm import Session

from app.database.repositories.base_repository import BaseRepository
from app.models.report import MedicalReport


class ReportRepository(BaseRepository[MedicalReport]):
    def __init__(self, db: Session):
        super().__init__(MedicalReport, db)

    def list_for_user(self, user_id: UUID) -> list[MedicalReport]:
        return self.db.query(MedicalReport).filter(MedicalReport.user_id == user_id).all()
