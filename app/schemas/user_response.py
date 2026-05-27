"""
User response schema.
"""

from datetime import datetime
from uuid import UUID

from app.schemas.user_base import UserBase


class UserResponse(UserBase):
    """User response model."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}