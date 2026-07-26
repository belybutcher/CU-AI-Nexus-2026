"""
Generic repository base class (Repository Pattern).

Encapsulates common CRUD operations so concrete repositories (UserRepository,
PredictionRepository, ...) only need to add domain-specific queries. Services
depend on repositories, never on the ORM Session directly outside this layer.
"""
from typing import Generic, Optional, Type, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """Generic CRUD repository parametrized over a SQLAlchemy model class."""

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get(self, id_: UUID) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == id_).first()

    def list(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: ModelType) -> None:
        self.db.delete(obj)
        self.db.commit()
