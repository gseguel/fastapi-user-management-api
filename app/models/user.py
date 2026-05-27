"""
User ORM model.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Enum, String
from sqlalchemy.orm import Mapped

from app.db.database import Base
from app.models.enums import UserRole


class User(Base):
    """User entity."""

    __tablename__ = "users"

    id: Mapped[str] = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )

    username: Mapped[str] = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    email: Mapped[str] = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    first_name: Mapped[str] = Column(
        String,
        nullable=False,
    )

    last_name: Mapped[str] = Column(
        String,
        nullable=False,
    )

    role: Mapped[UserRole] = Column(
        Enum(UserRole),
        default=UserRole.user,
        nullable=False,
    )

    active: Mapped[bool] = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username}>"