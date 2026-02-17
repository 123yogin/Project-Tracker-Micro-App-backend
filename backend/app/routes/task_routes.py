from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models.project import Project
from app.models.task import Task


task_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")


def _parse_due_date(value):
    if value in (None, ""):
        return None

    try:
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValueError("Invalid due_date format. Use ISO format, e.g., 2024-12-31T23:59:00")


@task_bp.post("")
@jwt_required()
def create_task():
    payload = request.get_json(silent=True) or {}
    title = (payload.get("title") or "").strip()
    project_id = payload.get("project_id")

    if not title or not project_id:
        return jsonify({"error": "Task title and project_id are required."}), 400

    user_id = int(get_jwt_identity())
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()
    if not project:
        return jsonify({"error": "Project not found."}), 404

    try:
        due_date = _parse_due_date(payload.get("due_date"))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    task = Task(
        title=title,
        description=payload.get("description"),
        status=(payload.get("status") or "pending").strip() or "pending",
        priority=payload.get("priority"),
        due_date=due_date,
        project_id=project.id,
    )

    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@task_bp.get("/<int:project_id>")
@jwt_required()
def list_tasks(project_id: int):
    user_id = int(get_jwt_identity())
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()
    if not project:
        return jsonify({"error": "Project not found."}), 404

    tasks = Task.query.filter_by(project_id=project_id).order_by(Task.created_at.desc()).all()
    return jsonify([task.to_dict() for task in tasks])


@task_bp.put("/<int:task_id>")
@jwt_required()
def update_task(task_id: int):
    user_id = int(get_jwt_identity())
    task = (
        Task.query.join(Project, Task.project_id == Project.id)
        .filter(Task.id == task_id, Project.user_id == user_id)
        .first()
    )

    if not task:
        return jsonify({"error": "Task not found."}), 404

    payload = request.get_json(silent=True) or {}

    if "title" in payload:
        title = (payload.get("title") or "").strip()
        if not title:
            return jsonify({"error": "Task title cannot be empty."}), 400
        task.title = title

    if "description" in payload:
        task.description = payload.get("description")

    if "status" in payload:
        task.status = (payload.get("status") or "pending").strip() or "pending"

    if "priority" in payload:
        task.priority = payload.get("priority")

    if "due_date" in payload:
        try:
            task.due_date = _parse_due_date(payload.get("due_date"))
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400

    db.session.commit()
    return jsonify(task.to_dict())


@task_bp.delete("/<int:task_id>")
@jwt_required()
def delete_task(task_id: int):
    user_id = int(get_jwt_identity())
    task = (
        Task.query.join(Project, Task.project_id == Project.id)
        .filter(Task.id == task_id, Project.user_id == user_id)
        .first()
    )

    if not task:
        return jsonify({"error": "Task not found."}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully."})
