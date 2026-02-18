"""Models package — import all models here for Alembic auto-detection."""

from app.models.project import Project
from app.models.task import Task
from app.models.user import User

__all__ = ["User", "Project", "Task"]
