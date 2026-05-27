"""
User creation schema.

Inherits all fields from UserBase.
"""

from app.schemas.user_base import UserBase


class UserCreate(UserBase):
    """User creation request schema."""
    pass