"""Health-check endpoint, used by load balancers / container orchestrators."""
from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Service health check")
async def health() -> dict:
    """Return basic liveness information. Extend with DB/model readiness checks as needed."""
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}
