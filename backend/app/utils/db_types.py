"""
Cross-database UUID column type.

PostgreSQL has a native UUID type; SQLite does not. This TypeDecorator stores
UUIDs as native UUID on Postgres and as CHAR(36) strings on SQLite, so the
same model definitions work against both backends without change.
"""
import uuid

from sqlalchemy import CHAR, TypeDecorator
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class GUID(TypeDecorator):
    """Platform-independent UUID type."""

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if dialect.name == "postgresql":
            return str(value)
        if not isinstance(value, uuid.UUID):
            return str(uuid.UUID(value))
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            return uuid.UUID(value)
        return value
