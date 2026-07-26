"""
Single import point that registers every ORM model on `Base.metadata`.

Anything that needs the *full* schema present — `Base.metadata.create_all()`
in `app/main.py`'s lifespan, or Alembic's `env.py` for autogeneration — should
`import app.models` (or `from app.models import *`) rather than importing
individual model modules, so a newly added model is never silently missing.

Whenever a new model file is added under `app/models/`, add its import here too.
"""
from app.models.user import User
from app.models.patient import Patient
from app.models.prediction import Prediction
from app.models.report import MedicalReport
from app.models.chat_history import ChatHistory

__all__ = ["User", "Patient", "Prediction", "MedicalReport", "ChatHistory"]
