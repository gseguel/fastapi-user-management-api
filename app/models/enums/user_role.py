"""User roles."""

import enum


class UserRole(str, enum.Enum):
    """Available user roles."""

    admin = "admin"
    user = "user"
    guest = "guest"