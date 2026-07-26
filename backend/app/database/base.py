"""
Declarative base class shared by every SQLAlchemy ORM model.

Deliberately contains NO model imports (models import `Base` *from* this
module, so importing models here too would create a circular import).
To ensure every model registers itself on `Base.metadata` (required for
`create_all()` and Alembic autogeneration), import the `app.models` package
instead — see `app/models/__init__.py`.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Shared declarative base class for all SQLAlchemy models."""
    pass
