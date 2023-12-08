from __future__ import with_statement
from flask import current_app
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from typing import Any

# Configuration dictionary for Alembic
config: dict[str, Any] = context.config

# Load logging configuration from the Alembic configuration file
fileConfig(config.config_file_name)

# Metadata object from the Flask SQLAlchemy extension, used for generating migrations
target_metadata = current_app.extensions['migrate'].db.metadata

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This function is used when running migrations in an environment without a
    live database connection, typically for generating migration scripts.
    """
    url: str = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    This function is used when running migrations with a live database connection.
    It handles the setup of the database connection and runs the migration commands.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

# Conditional logic to determine offline or online mode for migrations
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
