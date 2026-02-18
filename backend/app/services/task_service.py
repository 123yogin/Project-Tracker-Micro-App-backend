"""Task service — CRUD operations for tasks within projects."""

import logging

from app.extensions import db
from app.models.project import Project
from app.models.task import Task
from app.services.base import get_user_project_or_404, paginate_query
from app.utils.exceptions import NotFoundError

logger = logging.getLogger(__name__)


def _get_user_task(task_id: int, user_id: int) -> Task:
    """Fetch a task owned (via project) by user_id or raise NotFoundError."""
    task = (
        Task.query
        .join(Project, Task.project_id == Project.id)
        .filter(Task.id == task_id, Project.user_id == user_id)
        .first()
    )
    if not task:
        raise NotFoundError("Task not found.")
    return task


class TaskService:
    @staticmethod
    def create(user_id: int, data: dict) -> dict:
        project = get_user_project_or_404(data["project_id"], user_id)

        task = Task(
            title=data["title"],
            description=data.get("description"),
            status=data.get("status", "pending"),
            priority=data.get("priority"),
            due_date=data.get("due_date"),
            project_id=project.id,
        )
        db.session.add(task)
        db.session.commit()
        logger.info("Task created: id=%s project_id=%s", task.id, project.id)
        return task.to_dict()

    @staticmethod
    def list_for_project(
        user_id: int, project_id: int, page: int = 1, per_page: int = 20
    ) -> dict:
        get_user_project_or_404(project_id, user_id)

        query = (
            Task.query
            .filter_by(project_id=project_id)
            .order_by(Task.created_at.desc())
        )
        return paginate_query(query, page, per_page)

    @staticmethod
    def update(task_id: int, user_id: int, data: dict) -> dict:
        task = _get_user_task(task_id, user_id)

        if "title" in data:
            task.title = data["title"]
        if "description" in data:
            task.description = data["description"]
        if "status" in data:
            task.status = data["status"]
        if "priority" in data:
            task.priority = data["priority"]
        if "due_date" in data:
            task.due_date = data["due_date"]

        db.session.commit()
        logger.info("Task updated: id=%s", task_id)
        return task.to_dict()

    @staticmethod
    def delete(task_id: int, user_id: int) -> None:
        task = _get_user_task(task_id, user_id)
        db.session.delete(task)
        db.session.commit()
        logger.info("Task deleted: id=%s", task_id)
