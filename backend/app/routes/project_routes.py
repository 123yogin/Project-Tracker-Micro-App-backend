from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models.project import Project


project_bp = Blueprint("projects", __name__, url_prefix="/api/projects")


@project_bp.post("")
@jwt_required()
def create_project():
    payload = request.get_json(silent=True) or {}
    name = (payload.get("name") or "").strip()

    if not name:
        return jsonify({"error": "Project name is required."}), 400

    project = Project(
        name=name,
        description=payload.get("description"),
        user_id=int(get_jwt_identity()),
    )
    db.session.add(project)
    db.session.commit()

    return jsonify(project.to_dict()), 201


@project_bp.get("")
@jwt_required()
def list_projects():
    user_id = int(get_jwt_identity())
    projects = Project.query.filter_by(user_id=user_id).order_by(Project.created_at.desc()).all()
    return jsonify([project.to_dict() for project in projects])


@project_bp.get("/<int:project_id>")
@jwt_required()
def get_project(project_id: int):
    user_id = int(get_jwt_identity())
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()

    if not project:
        return jsonify({"error": "Project not found."}), 404

    return jsonify(project.to_dict(include_tasks=True))


@project_bp.put("/<int:project_id>")
@jwt_required()
def update_project(project_id: int):
    user_id = int(get_jwt_identity())
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()

    if not project:
        return jsonify({"error": "Project not found."}), 404

    payload = request.get_json(silent=True) or {}

    if "name" in payload:
        name = (payload.get("name") or "").strip()
        if not name:
            return jsonify({"error": "Project name cannot be empty."}), 400
        project.name = name

    if "description" in payload:
        project.description = payload.get("description")

    db.session.commit()
    return jsonify(project.to_dict())


@project_bp.delete("/<int:project_id>")
@jwt_required()
def delete_project(project_id: int):
    user_id = int(get_jwt_identity())
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()

    if not project:
        return jsonify({"error": "Project not found."}), 404

    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted successfully."})
