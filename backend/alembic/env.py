"""
Alembic migration environment.

Uses the same `DATABASE_URL` as the running application (via `app.core.config.settings`)
so migrations always target the correct database, and imports `Base.metadata`
from `app.database.base` (which in turn imports every model) so
`alembic revision --autogenerate` picks up all tables.
"""
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# Make the `app` package importable when running `alembic` from the backend/ root.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.config import settings
import app.models  # noqa: F401  (registers all models on Base.metadata)
from app.database.base import Base

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (emits SQL without a live DB connection)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (against a live DB connection)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
