"""
Centralized logging configuration.

Configures application-wide logging.
"""

import logging


def setup_logging() -> None:
    """Configure logging format and level."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    logging.getLogger(__name__).info("Logging configured")