"""Search service for finding projects and tasks."""

from sqlalchemy import or_

from app.models.project import Project
from app.models.task import Task
from app.extensions import db


class SearchService:
    @staticmethod
    def search(user_id: int, query: str) -> dict:
        """Search projects and tasks for a given query string."""
        if not query or len(query.strip()) < 2:
            return {"projects": [], "tasks": []}

        search_term = f"%{query}%"

        # Search projects
        projects = Project.query.filter(
            Project.user_id == user_id,
            or_(
                Project.name.ilike(search_term),
                Project.description.ilike(search_term)
            )
        ).limit(5).all()

        # Search tasks (ensure they belong to user's projects)
        tasks = Task.query.join(Project).filter(
            Project.user_id == user_id,
            or_(
                Task.title.ilike(search_term),
                Task.description.ilike(search_term)
            )
        ).limit(10).all()

        return {
            "projects": [p.to_dict() for p in projects],
            "tasks": [t.to_dict() for t in tasks]
        }
