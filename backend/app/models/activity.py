"""Activity Log model for audit trails."""

from datetime import datetime, timezone

from app.extensions import db


class ActivityLog(db.Model):
    __tablename__ = "activity_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    action = db.Column(db.String(50), nullable=False)  # created, updated, deleted
    target_type = db.Column(db.String(50), nullable=False)  # project, task
    target_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.JSON, nullable=True)  # Snapshot of change
    ip_address = db.Column(db.String(45), nullable=True)
    timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    user = db.relationship("User", back_populates="activities")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "action": self.action,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
        }
