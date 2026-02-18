"""Notification routes."""

from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models.notification import Notification

notification_bp = Blueprint("notifications", __name__, url_prefix="/api/notifications")

@notification_bp.route("/", methods=["GET"])
@jwt_required()
def get_notifications():
    """Get unread notifications."""
    user_id = get_jwt_identity()
    notifications = Notification.query.filter_by(user_id=user_id, read=False)\
        .order_by(Notification.created_at.desc()).limit(50).all()
    return jsonify([n.to_dict() for n in notifications]), 200

@notification_bp.route("/<int:n_id>/read", methods=["POST"])
@jwt_required()
def mark_read(n_id):
    """Mark a notification as read."""
    user_id = get_jwt_identity()
    notification = Notification.query.filter_by(id=n_id, user_id=user_id).first()
    if notification:
        notification.read = True
        db.session.commit()
    return jsonify({"success": True}), 200

@notification_bp.route("/read-all", methods=["POST"])
@jwt_required()
def mark_all_read():
    """Mark all notifications as read."""
    user_id = get_jwt_identity()
    Notification.query.filter_by(user_id=user_id, read=False).update({"read": True})
    db.session.commit()
    return jsonify({"success": True}), 200
