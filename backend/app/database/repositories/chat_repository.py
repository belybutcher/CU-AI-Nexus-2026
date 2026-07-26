"""Repository for ChatHistory persistence and lookups."""
from uuid import UUID

from sqlalchemy.orm import Session

from app.database.repositories.base_repository import BaseRepository
from app.models.chat_history import ChatHistory


class ChatRepository(BaseRepository[ChatHistory]):
    def __init__(self, db: Session):
        super().__init__(ChatHistory, db)

    def list_for_user(self, user_id: UUID, skip: int = 0, limit: int = 100) -> list[ChatHistory]:
        return (
            self.db.query(ChatHistory)
            .filter(ChatHistory.user_id == user_id)
            .order_by(ChatHistory.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
