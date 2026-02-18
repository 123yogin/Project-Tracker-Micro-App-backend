"""Application configuration loaded from environment variables."""

import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(32).hex())

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///project_tracker.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.environ.get("JWT_ACCESS_MINUTES", "60"))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.environ.get("JWT_REFRESH_DAYS", "30"))
    )
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"

    CORS_ORIGINS = os.environ.get(
        "CORS_ORIGINS", "http://localhost:5173"
    ).split(",")

    RATELIMIT_DEFAULT = "200/hour"
    RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")

    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

    PASSWORD_MIN_LENGTH = int(os.environ.get("PASSWORD_MIN_LENGTH", "8"))

    @staticmethod
    def init_app(app):
        """Validate critical settings at startup."""
        if not app.config.get("JWT_SECRET_KEY"):
            if not app.config.get("DEBUG"):
                raise RuntimeError(
                    "JWT_SECRET_KEY must be set via environment variable."
                )
            import secrets
            generated = secrets.token_urlsafe(64)
            app.config["JWT_SECRET_KEY"] = generated
            app.logger.warning(
                "Generated a random JWT_SECRET_KEY for this session. "
                "Set JWT_SECRET_KEY in .env for stable tokens."
            )
