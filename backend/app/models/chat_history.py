"""ChatHistory ORM model — one turn of the medical assistant chatbot."""
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.utils.db_types import GUID


class ChatHistory(Base):
    """A single question/answer exchange with the AI medical assistant."""

    __tablename__ = "chat_history"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("users.id"), nullable=False)
    prediction_id: Mapped[uuid.UUID | None] = mapped_column(GUID(), ForeignKey("predictions.id"), nullable=True)

    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    retrieved_context: Mapped[list] = mapped_column(JSON, default=list)  # snippets used by the RAG pipeline

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user: Mapped["User"] = relationship(back_populates="chat_messages")
