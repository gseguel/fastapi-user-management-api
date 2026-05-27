"""
Base user schema.

Shared fields and validation for user-related schemas.
"""

import re
from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.enums import UserRole


class UserBase(BaseModel):
    """Shared user fields and validation rules."""

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        examples=["gseguel"],
    )

    email: EmailStr = Field(
        ...,
        examples=["gseguel@example.com"],
    )

    first_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["Gustavo"],
    )

    last_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["Seguel"],
    )

    role: UserRole = Field(
        UserRole.user,
        examples=["user"],
    )

    active: bool = Field(
        True,
        examples=[True],
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        """Validate username format."""

        if not re.match(
            r"^[a-zA-Z0-9]([a-zA-Z0-9_-]*[a-zA-Z0-9])?$",
            value,
        ):
            raise ValueError(
                "Username must contain only letters, numbers, "
                "hyphens and underscores, and start/end with "
                "a letter or number."
            )

        return value.lower()