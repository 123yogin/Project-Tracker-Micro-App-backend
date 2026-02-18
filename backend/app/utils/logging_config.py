"""Application logging configuration."""

import logging
import sys
from logging.handlers import RotatingFileHandler


def setup_logging(app):
    """Configure application logging based on config."""
    log_level = app.config.get("LOG_LEVEL", "INFO").upper()
    numeric_level = getattr(logging, log_level, logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Clear default Flask handlers FIRST to avoid duplicates
    app.logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(numeric_level)
    app.logger.addHandler(console_handler)

    # File handler — rotate at 10 MB, keep 5 backups
    try:
        file_handler = RotatingFileHandler(
            "app.log", maxBytes=10_000_000, backupCount=5
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
    except OSError:
        app.logger.warning("Could not create log file — using console only.")

    app.logger.setLevel(numeric_level)

    # Suppress noisy Werkzeug per-request logging in production
    if numeric_level > logging.DEBUG:
        logging.getLogger("werkzeug").setLevel(logging.WARNING)

    app.logger.info("Logging initialised at level %s", log_level)
