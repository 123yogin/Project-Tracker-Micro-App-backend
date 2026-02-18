"""User model."""

from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(100), nullable=True)  # Added for SaaS profile
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    last_login = db.Column(db.DateTime, nullable=True)  # Added for security audit

    projects = db.relationship(
        "Project",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )
    
    activities = db.relationship(
        "ActivityLog",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
        order_by="desc(ActivityLog.timestamp)"
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(
            password, method="pbkdf2:sha256:600000"
        )

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }
