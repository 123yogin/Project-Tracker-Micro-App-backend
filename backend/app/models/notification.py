"""Notification model for user alerts."""

from datetime import datetime, timezone
from app.extensions import db

class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    type = db.Column(db.String(50), nullable=False)  # info, success, warning, error
    message = db.Column(db.String(255), nullable=False)
    read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "message": self.message,
            "read": self.read,
            "created_at": self.created_at.isoformat(),
        }
