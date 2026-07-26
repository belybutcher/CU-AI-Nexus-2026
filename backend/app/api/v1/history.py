"""Patient/prediction history endpoints."""
import logging
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.history import HistoryListResponse
from app.services.history_service import HistoryService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["History"])


@router.get("/history", response_model=HistoryListResponse, summary="List the current user's diagnostic history")
async def get_history(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> HistoryListResponse:
    """Return the current user's prediction history, most recent first."""
    return HistoryService(db).get_history(current_user.id, skip=skip, limit=limit)


@router.delete("/history/{prediction_id}", status_code=204, summary="Delete a history entry")
async def delete_history_item(
    prediction_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a prediction from the current user's history."""
    HistoryService(db).delete_history_item(current_user.id, prediction_id)
