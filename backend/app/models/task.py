"""Task model with indexed FK."""

from datetime import datetime, timezone

from app.constants import TASK_PRIORITIES, TASK_STATUSES  # noqa: F401 – re-export for backwards compat
from app.extensions import db


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default="pending", nullable=False)
    priority = db.Column(db.String(50), nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    project_id = db.Column(
        db.Integer,
        db.ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    project = db.relationship("Project", back_populates="tasks")
    comments = db.relationship(
        "Comment",
        back_populates="task",
        cascade="all, delete-orphan",
        lazy="select",
        order_by="asc(Comment.created_at)"
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat(),
            "project_id": self.project_id,
        }
