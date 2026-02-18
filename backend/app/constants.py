"""Shared constants used across models and schemas.

Single source of truth — import from here, never duplicate.
"""

TASK_STATUSES = ("pending", "in_progress", "completed", "cancelled")
TASK_PRIORITIES = ("low", "medium", "high", "critical")
