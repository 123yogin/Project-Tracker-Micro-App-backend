"""Authentication service — registration, login, token management."""

import logging

from flask_jwt_extended import create_access_token, create_refresh_token

from app.extensions import db
from app.models.user import User
from app.utils.exceptions import AuthenticationError, ConflictError

logger = logging.getLogger(__name__)


class AuthService:
    @staticmethod
    def register(email: str, password: str) -> dict:
        """Create a new user and return tokens + user data."""
        email = email.strip().lower()

        if User.query.filter_by(email=email).first():
            raise ConflictError("Email is already registered.")

        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        logger.info("User registered: id=%s", user.id)

        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            "message": "User registered successfully.",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict(),
        }

    @staticmethod
    def login(email: str, password: str) -> dict:
        """Authenticate a user and return tokens + user data."""
        email = email.strip().lower()

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            logger.warning("Failed login attempt for email=%s", email)
            raise AuthenticationError("Invalid email or password.")

        logger.info("Successful login: user_id=%s", user.id)

        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            "message": "Login successful.",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict(),
        }
