"""Repository for Patient persistence and lookups."""
from uuid import UUID

from sqlalchemy.orm import Session

from app.database.repositories.base_repository import BaseRepository
from app.models.patient import Patient


class PatientRepository(BaseRepository[Patient]):
    def __init__(self, db: Session):
        super().__init__(Patient, db)

    def list_for_owner(self, owner_id: UUID) -> list[Patient]:
        return self.db.query(Patient).filter(Patient.owner_id == owner_id).all()
