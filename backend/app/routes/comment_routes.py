"""Comment routes for tasks."""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models.comment import Comment
from app.models.task import Task
from app.models.project import Project
from app.utils.responses import error_response

comment_bp = Blueprint("comments", __name__, url_prefix="/api/tasks")

@comment_bp.route("/<int:task_id>/comments", methods=["GET"])
@jwt_required()
def get_comments(task_id):
    """Get comments for a task."""
    user_id = get_jwt_identity()
    
    # Verify access to task (via project ownership)
    task = Task.query.join(Project).filter(Task.id == task_id, Project.user_id == user_id).first()
    if not task:
        return error_response("Task not found", 404)
        
    comments = Comment.query.filter_by(task_id=task_id).order_by(Comment.created_at.asc()).all()
    return jsonify([c.to_dict() for c in comments]), 200

@comment_bp.route("/<int:task_id>/comments", methods=["POST"])
@jwt_required()
def add_comment(task_id):
    """Add a comment to a task."""
    user_id = get_jwt_identity()
    data = request.json
    
    if not data or not data.get("content"):
        return error_response("Content is required", 400)

    # Verify access
    task = Task.query.join(Project).filter(Task.id == task_id, Project.user_id == user_id).first()
    if not task:
        return error_response("Task not found", 404)

    comment = Comment(
        content=data["content"],
        task_id=task_id,
        user_id=user_id
    )
    db.session.add(comment)
    db.session.commit()
    
    return jsonify(comment.to_dict()), 201
