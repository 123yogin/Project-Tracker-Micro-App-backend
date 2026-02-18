"""Models package — import all models here for Alembic auto-detection."""

from app.models.activity import ActivityLog
from app.models.comment import Comment
from app.models.notification import Notification
from app.models.project import Project
from app.models.task import Task
from app.models.user import User

__all__ = ["User", "Project", "Task", "ActivityLog", "Comment", "Notification"]
