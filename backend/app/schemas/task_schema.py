"""Task request validation schemas."""

from marshmallow import Schema, fields, validate

from app.constants import TASK_PRIORITIES, TASK_STATUSES


class CreateTaskSchema(Schema):
    title = fields.String(
        required=True,
        validate=validate.Length(min=1, max=255, error="Task title must be 1–255 characters."),
        error_messages={"required": "Task title is required."},
    )
    description = fields.String(
        validate=validate.Length(max=2000),
        load_default=None,
        allow_none=True,
    )
    status = fields.String(
        validate=validate.OneOf(TASK_STATUSES, error="Status must be one of: {choices}."),
        load_default="pending",
    )
    priority = fields.String(
        validate=validate.OneOf(TASK_PRIORITIES, error="Priority must be one of: {choices}."),
        load_default=None,
        allow_none=True,
    )
    due_date = fields.DateTime(load_default=None, allow_none=True, format="iso")
    project_id = fields.Integer(
        required=True,
        error_messages={"required": "project_id is required."},
    )


class UpdateTaskSchema(Schema):
    title = fields.String(validate=validate.Length(min=1, max=255))
    description = fields.String(validate=validate.Length(max=2000), allow_none=True)
    status = fields.String(
        validate=validate.OneOf(TASK_STATUSES, error="Status must be one of: {choices}."),
    )
    priority = fields.String(
        validate=validate.OneOf(TASK_PRIORITIES, error="Priority must be one of: {choices}."),
        allow_none=True,
    )
    due_date = fields.DateTime(allow_none=True, format="iso")
