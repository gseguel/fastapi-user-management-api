"""
Paginated user list response schema.
"""

from pydantic import BaseModel

from app.schemas.user_response import UserResponse


class UserListResponse(BaseModel):
    """Paginated user list response."""

    total: int
    users: list[UserResponse]