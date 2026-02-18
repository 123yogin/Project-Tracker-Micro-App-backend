"""Project routes — thin controllers delegating to ProjectService."""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError as MarshmallowValidationError

from app.schemas.project_schema import (
    CreateProjectSchema,
    PaginationSchema,
    UpdateProjectSchema,
)
from app.services.project_service import ProjectService
from app.utils.responses import error_response

project_bp = Blueprint("projects", __name__, url_prefix="/api/projects")

_create_schema = CreateProjectSchema()
_update_schema = UpdateProjectSchema()
_pagination_schema = PaginationSchema()


@project_bp.post("")
@jwt_required()
def create_project():
    user_id = int(get_jwt_identity())
    payload = request.get_json(silent=True) or {}

    try:
        data = _create_schema.load(payload)
    except MarshmallowValidationError as exc:
        return error_response("Validation failed.", 400, exc.messages)

    result = ProjectService.create(user_id, data["name"], data.get("description"))
    return jsonify(result), 201


@project_bp.get("")
@jwt_required()
def list_projects():
    user_id = int(get_jwt_identity())

    try:
        params = _pagination_schema.load(request.args.to_dict())
    except MarshmallowValidationError as exc:
        return error_response("Invalid pagination parameters.", 400, exc.messages)

    result = ProjectService.list_for_user(
        user_id, page=params["page"], per_page=params["per_page"]
    )
    return jsonify(result), 200


@project_bp.get("/<int:project_id>")
@jwt_required()
def get_project(project_id: int):
    user_id = int(get_jwt_identity())
    result = ProjectService.get(project_id, user_id)
    return jsonify(result), 200


@project_bp.put("/<int:project_id>")
@jwt_required()
def update_project(project_id: int):
    user_id = int(get_jwt_identity())
    payload = request.get_json(silent=True) or {}

    try:
        data = _update_schema.load(payload)
    except MarshmallowValidationError as exc:
        return error_response("Validation failed.", 400, exc.messages)

    if not data:
        return error_response("No fields to update.", 400)

    result = ProjectService.update(project_id, user_id, data)
    return jsonify(result), 200


@project_bp.delete("/<int:project_id>")
@jwt_required()
def delete_project(project_id: int):
    user_id = int(get_jwt_identity())
    ProjectService.delete(project_id, user_id)
    return jsonify({"message": "Project deleted successfully."}), 200
