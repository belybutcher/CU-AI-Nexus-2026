"""Business logic for the AI medical assistant chatbot."""
import uuid

from sqlalchemy.orm import Session

from app.ai.chatbot import rag_pipeline
from app.core.exceptions import NotFoundException
from app.database.repositories.chat_repository import ChatRepository
from app.database.repositories.prediction_repository import PredictionRepository
from app.models.chat_history import ChatHistory
from app.schemas.chat import ChatRequest, ChatResponse


class ChatbotService:
    """Orchestrates the retrieve -> build_prompt -> generate_answer RAG flow."""

    def __init__(self, db: Session):
        self.db = db
        self.chat_repo = ChatRepository(db)
        self.prediction_repo = PredictionRepository(db)

    def chat(self, user_id: uuid.UUID, payload: ChatRequest) -> ChatResponse:
        """Answer a clinician's question, optionally grounded in a prior prediction."""
        prediction_context = None
        if payload.prediction_id:
            prediction = self.prediction_repo.get(payload.prediction_id)
            if not prediction:
                raise NotFoundException(f"Prediction '{payload.prediction_id}' not found.")
            prediction_context = {
                "disease": prediction.disease,
                "predicted_label": prediction.predicted_label,
                "confidence": prediction.confidence,
            }

        context = rag_pipeline.retrieve_context(payload.question, prediction_context)
        prompt = rag_pipeline.build_prompt(payload.question, context, prediction_context)
        answer = rag_pipeline.generate_answer(prompt)

        chat_entry = ChatHistory(
            user_id=user_id,
            prediction_id=payload.prediction_id,
            question=payload.question,
            answer=answer,
            retrieved_context=context,
        )
        self.chat_repo.create(chat_entry)

        return ChatResponse(
            id=chat_entry.id,
            question=chat_entry.question,
            answer=chat_entry.answer,
            retrieved_context=chat_entry.retrieved_context,
            created_at=chat_entry.created_at,
        )
