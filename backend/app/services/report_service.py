"""
Business logic for generating downloadable diagnostic reports.

Produces a simple PDF or HTML summary of a prediction. This is intentionally
basic (not a clinical report template) — swap `_render_pdf`/`_render_html`
for a proper templated report (e.g. with a hospital letterhead, Jinja2 HTML
-> WeasyPrint PDF) without touching the rest of the service.
"""
import uuid
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import NotFoundException
from app.database.repositories.prediction_repository import PredictionRepository
from app.database.repositories.report_repository import ReportRepository
from app.models.prediction import Prediction
from app.models.report import MedicalReport
from app.schemas.report import GenerateReportRequest, ReportResponse
from app.utils.file_utils import build_storage_relative_path


class ReportService:
    """Renders and persists diagnostic reports for a given prediction."""

    def __init__(self, db: Session):
        self.db = db
        self.prediction_repo = PredictionRepository(db)
        self.report_repo = ReportRepository(db)

    def generate_report(self, user_id: uuid.UUID, payload: GenerateReportRequest) -> ReportResponse:
        """Build a report file for a prediction and persist its metadata."""
        prediction = self.prediction_repo.get(payload.prediction_id)
        if not prediction:
            raise NotFoundException(f"Prediction '{payload.prediction_id}' not found.")

        summary = self._build_summary(prediction)
        destination = settings.storage_path(settings.REPORT_DIR) / f"{uuid.uuid4()}.{payload.file_format}"

        if payload.file_format == "pdf":
            self._render_pdf(destination, summary, prediction)
        else:
            self._render_html(destination, summary, prediction)

        report = MedicalReport(
            user_id=user_id,
            prediction_id=prediction.id,
            file_path=build_storage_relative_path(destination),
            file_format=payload.file_format,
            summary=summary,
        )
        self.report_repo.create(report)

        return self._to_response(report)

    def get_report(self, report_id: uuid.UUID) -> ReportResponse:
        """Fetch a previously generated report by id."""
        report = self.report_repo.get(report_id)
        if not report:
            raise NotFoundException(f"Report '{report_id}' not found.")
        return self._to_response(report)

    @staticmethod
    def _build_summary(prediction: Prediction) -> str:
        return (
            f"Modality: {prediction.modality} | Disease: {prediction.disease}\n"
            f"Predicted label: {prediction.predicted_label} "
            f"(confidence: {prediction.confidence:.1%})\n"
            f"Model version: {prediction.model_version}\n"
            f"Generated: {prediction.created_at.isoformat()}\n\n"
            "This AI-assisted report is intended to support, not replace, "
            "review by a qualified clinician."
        )

    @staticmethod
    def _render_html(destination: Path, summary: str, prediction: Prediction) -> None:
        html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>CU AI Nexus Report</title></head>
<body>
<h1>Diagnostic Report</h1>
<pre>{summary}</pre>
</body></html>"""
        destination.write_text(html, encoding="utf-8")

    @staticmethod
    def _render_pdf(destination: Path, summary: str, prediction: Prediction) -> None:
        """
        Render a minimal PDF using fpdf2.

        TODO: replace with a proper clinical report template (letterhead,
        embedded original/enhanced/heatmap images, structured tables).
        """
        from fpdf import FPDF

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=14)
        pdf.cell(0, 10, "CU AI Nexus - Diagnostic Report", ln=True)
        pdf.set_font("Helvetica", size=11)
        pdf.ln(4)
        for line in summary.split("\n"):
            pdf.multi_cell(0, 7, line)
        pdf.output(str(destination))

    @staticmethod
    def _to_response(report: MedicalReport) -> ReportResponse:
        return ReportResponse(
            id=report.id,
            prediction_id=report.prediction_id,
            file_path=report.file_path,
            file_format=report.file_format,
            summary=report.summary,
            created_at=report.created_at,
        )
