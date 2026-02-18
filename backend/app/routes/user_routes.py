"""User profile and settings routes."""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models.user import User
from app.services.activity_service import ActivityService
from app.utils.responses import error_response

user_bp = Blueprint("user", __name__, url_prefix="/users")


@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_profile():
    """Get current user profile."""
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user:
        return error_response("User not found", 404)
    return jsonify(user.to_dict()), 200


@user_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_profile():
    """Update user profile details."""
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user:
        return error_response("User not found", 404)

    data = request.json
    if "full_name" in data:
        user.full_name = data["full_name"]
    
    # We could allow email updates here too, but that requires re-verification logic.
    # For MVP SaaS, we'll skip email change for now to avoid security complexity.

    db.session.commit()
    return jsonify(user.to_dict()), 200


@user_bp.route("/activity", methods=["GET"])
@jwt_required()
def get_activity():
    """Get recent user activity."""
    user_id = get_jwt_identity()
    activities = ActivityService.get_recent_activity(user_id)
    return jsonify([a.to_dict() for a in activities]), 200
