"""Project service — CRUD operations for projects."""

import logging

from app.extensions import db
from app.models.project import Project
from app.services.activity_service import ActivityService
from app.services.base import get_user_project_or_404, paginate_query

logger = logging.getLogger(__name__)


class ProjectService:
    @staticmethod
    def create(user_id: int, name: str, description: str | None = None) -> dict:
        project = Project(name=name, description=description, user_id=user_id)
        db.session.add(project)
        db.session.commit()
        ActivityService.log(user_id, "created", "project", project.id, {"name": name})
        logger.info("Project created: id=%s user_id=%s", project.id, user_id)
        return project.to_dict()

    @staticmethod
    def list_for_user(user_id: int, page: int = 1, per_page: int = 20) -> dict:
        query = (
            Project.query
            .filter_by(user_id=user_id)
            .order_by(Project.created_at.desc())
        )
        return paginate_query(query, page, per_page)

    @staticmethod
    def get(project_id: int, user_id: int) -> dict:
        project = get_user_project_or_404(project_id, user_id)
        return project.to_dict(include_tasks=True)

    @staticmethod
    def update(project_id: int, user_id: int, data: dict) -> dict:
        project = get_user_project_or_404(project_id, user_id)

        changes = {}
        if "name" in data:
            changes["old_name"] = project.name
            project.name = data["name"]
            changes["new_name"] = data["name"]
        if "description" in data:
            project.description = data["description"]

        db.session.commit()
        if changes:
             ActivityService.log(user_id, "updated", "project", project.id, changes)
        logger.info("Project updated: id=%s", project_id)
        return project.to_dict()

    @staticmethod
    def delete(project_id: int, user_id: int) -> None:
        project = get_user_project_or_404(project_id, user_id)
        name_snapshot = project.name
        db.session.delete(project)
        db.session.commit()
        ActivityService.log(user_id, "deleted", "project", project_id, {"name": name_snapshot})
        logger.info("Project deleted: id=%s", project_id)
