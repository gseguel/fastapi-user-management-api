"""
Application entry point.

FastAPI application, including:
- logging setup
- database initialization
- middleware and route registration
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core import settings, setup_logging, setup_middlewares
from app.db.database import init_db
from app.routes import users

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle events.

    Handles startup and shutdown operations such as:
    - Logging initialization
    - Database initialization
    """

    # Configure application logging
    setup_logging()

    logger.info("Starting application...")

    # Initialize database and create tables
    init_db()

    logger.info("Database initialized successfully.")

    yield

    logger.info("Shutting down application.")


app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# Register application middlewares
setup_middlewares(app)

# Register API routes
app.include_router(
    users.router,
    prefix="/api/v1",
    tags=["Users"],
)


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint.

    Returns the current application status.
    """

    return {
        "status": "ok",
        "message": "Application is running",
    }