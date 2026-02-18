"""Activity logging service."""

import logging
from datetime import datetime, timezone

from app.extensions import db
from app.models.activity import ActivityLog


class ActivityService:
    @staticmethod
    def log(user_id: int, action: str, target_type: str, target_id: int = None, details: dict = None, ip_address: str = None):
        """Create an audit log entry."""
        try:
            log_entry = ActivityLog(
                user_id=user_id,
                action=action,
                target_type=target_type,
                target_id=target_id,
                details=details,
                ip_address=ip_address,
                timestamp=datetime.now(timezone.utc)
            )
            db.session.add(log_entry)
            db.session.commit()
        except Exception as e:
            logging.error(f"Failed to log activity: {e}")
            db.session.rollback()

    @staticmethod
    def get_recent_activity(user_id: int, limit: int = 20):
        """Get recent activity for a user."""
        return ActivityLog.query.filter_by(user_id=user_id)\
            .order_by(ActivityLog.timestamp.desc())\
            .limit(limit)\
            .all()
