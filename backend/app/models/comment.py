"""Comment model for task discussions."""

from datetime import datetime, timezone
from app.extensions import db

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    task_id = db.Column(
        db.Integer,
        db.ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user = db.relationship("User", backref=db.backref("comments", lazy=True))
    task = db.relationship("Task", back_populates="comments")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "user_name": self.user.full_name or self.user.email.split('@')[0],
            "created_at": self.created_at.isoformat(),
        }
