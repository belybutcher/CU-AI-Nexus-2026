"""Report generation & retrieval endpoints."""
import logging
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.report import GenerateReportRequest, ReportResponse
from app.services.report_service import ReportService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Reports"])


@router.post("/generate-report", response_model=ReportResponse, status_code=201, summary="Generate a diagnostic report")
async def generate_report(
    payload: GenerateReportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ReportResponse:
    """Generate a downloadable PDF/HTML report summarizing a prediction."""
    return ReportService(db).generate_report(current_user.id, payload)


@router.get("/report/{report_id}", response_model=ReportResponse, summary="Fetch a generated report")
async def get_report(
    report_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ReportResponse:
    """Retrieve metadata about a previously generated report."""
    return ReportService(db).get_report(report_id)
