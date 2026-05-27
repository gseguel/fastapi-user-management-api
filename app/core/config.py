"""
Central application configuration.

Loads environment variables and exposes application settings.
"""

import os
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    """Application settings container."""

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./data/users.db",
    )

    # Metadata
    APP_TITLE: str = os.getenv("APP_TITLE", "User Management API")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    APP_DESCRIPTION: str = os.getenv(
        "APP_DESCRIPTION",
        "REST API for user management with full CRUD operations",
    )

    # CORS
    ALLOWED_ORIGINS: List[str] = None

    def __post_init__(self):
        origins = os.getenv("ALLOWED_ORIGINS", "*")

        self.ALLOWED_ORIGINS = (
            ["*"]
            if origins == "*"
            else [o.strip() for o in origins.split(",")]
        )


settings = Settings()