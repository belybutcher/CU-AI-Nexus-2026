"""UUID generation helper (kept centralized for consistency/testability)."""
import uuid


def new_uuid() -> uuid.UUID:
    """Generate a new random UUID4, used for all primary keys in the system."""
    return uuid.uuid4()
