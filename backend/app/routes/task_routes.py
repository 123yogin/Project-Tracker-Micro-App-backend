"""Task routes — thin controllers delegating to TaskService."""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError as MarshmallowValidationError

from app.schemas.project_schema import PaginationSchema
from app.schemas.task_schema import CreateTaskSchema, UpdateTaskSchema
from app.services.task_service import TaskService
from app.utils.responses import error_response

task_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")

_create_schema = CreateTaskSchema()
_update_schema = UpdateTaskSchema()
_pagination_schema = PaginationSchema()


@task_bp.post("")
@jwt_required()
def create_task():
    user_id = int(get_jwt_identity())
    payload = request.get_json(silent=True) or {}

    try:
        data = _create_schema.load(payload)
    except MarshmallowValidationError as exc:
        return error_response("Validation failed.", 400, exc.messages)

    result = TaskService.create(user_id, data)
    return jsonify(result), 201


@task_bp.get("/<int:project_id>")
@jwt_required()
def list_tasks(project_id: int):
    user_id = int(get_jwt_identity())

    try:
        params = _pagination_schema.load(request.args.to_dict())
    except MarshmallowValidationError as exc:
        return error_response("Invalid pagination parameters.", 400, exc.messages)

    result = TaskService.list_for_project(
        user_id, project_id, page=params["page"], per_page=params["per_page"]
    )
    return jsonify(result), 200


@task_bp.put("/<int:task_id>")
@jwt_required()
def update_task(task_id: int):
    user_id = int(get_jwt_identity())
    payload = request.get_json(silent=True) or {}

    try:
        data = _update_schema.load(payload)
    except MarshmallowValidationError as exc:
        return error_response("Validation failed.", 400, exc.messages)

    if not data:
        return error_response("No fields to update.", 400)

    result = TaskService.update(task_id, user_id, data)
    return jsonify(result), 200


@task_bp.delete("/<int:task_id>")
@jwt_required()
def delete_task(task_id: int):
    user_id = int(get_jwt_identity())
    TaskService.delete(task_id, user_id)
    return jsonify({"message": "Task deleted successfully."}), 200
