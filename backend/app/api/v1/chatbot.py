"""AI medical assistant chatbot endpoint."""
import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chatbot_service import ChatbotService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Chatbot"])


@router.post("/chat", response_model=ChatResponse, summary="Ask the AI medical assistant a question")
async def chat(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChatResponse:
    """Ask a question to the AI medical assistant, optionally grounded in a prior prediction."""
    return ChatbotService(db).chat(current_user.id, payload)
