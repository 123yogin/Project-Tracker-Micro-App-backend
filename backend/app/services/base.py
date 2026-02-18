"""Base service with shared ownership query and pagination helpers.

Eliminates the repeated `Project.query.filter_by(id=..., user_id=...).first()`
pattern and identical pagination dict construction across services.
"""

from app.extensions import db
from app.models.project import Project
from app.utils.exceptions import NotFoundError


def get_user_project_or_404(project_id: int, user_id: int) -> Project:
    """Fetch a project owned by user_id or raise NotFoundError."""
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()
    if not project:
        raise NotFoundError("Project not found.")
    return project


def paginate_query(query, page: int, per_page: int, serialize_fn=None) -> dict:
    """Run pagination on a query and return a standardised dict.

    `serialize_fn` defaults to calling `.to_dict()` on each item.
    """
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    items = [
        (serialize_fn(item) if serialize_fn else item.to_dict())
        for item in pagination.items
    ]
    return {
        "items": items,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages,
    }
