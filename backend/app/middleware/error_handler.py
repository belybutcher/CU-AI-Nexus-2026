"""
Convenience re-export so `app/main.py` has a single import for wiring up
all exception handlers (kept in `app.core.exceptions` to avoid a circular
import between `core` and `middleware`).
"""
from app.core.exceptions import register_exception_handlers  # noqa: F401
