"""
Database setup and session management.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


DATABASE_URL = settings.DATABASE_URL

# SQLite needs special thread handling
is_sqlite = DATABASE_URL.startswith("sqlite")

connect_args = (
    {"check_same_thread": False}
    if is_sqlite
    else {}
)

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    """Base class for ORM models."""
    pass


def init_db() -> None:
    """Create database tables."""

    # Create local SQLite directory if needed
    if is_sqlite:
        os.makedirs("data", exist_ok=True)

    # Import models before creating metadata
    from app.models.user import User  # noqa

    Base.metadata.create_all(bind=engine)


def get_db():
    """Provide a database session per request."""

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()