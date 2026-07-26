"""
Aggregates all v1 routers into a single APIRouter mounted by app/main.py
under the `/api/v1` prefix (see `app/core/config.py: API_V1_PREFIX`).

Routers are NOT given additional sub-prefixes so the final paths match the
spec exactly, e.g. `/api/v1/register`, `/api/v1/predict`, `/api/v1/history/{id}`.
"""
from fastapi import APIRouter

from app.api.v1 import auth, chatbot, diagnosis, health, history, images, reports

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(images.router)
api_router.include_router(diagnosis.router)
api_router.include_router(chatbot.router)
api_router.include_router(reports.router)
api_router.include_router(history.router)
