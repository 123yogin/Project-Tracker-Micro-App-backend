"""Project request validation schemas."""

from marshmallow import Schema, fields, validate


class CreateProjectSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=255, error="Project name must be 1–255 characters."),
        error_messages={"required": "Project name is required."},
    )
    description = fields.String(
        validate=validate.Length(max=2000),
        load_default=None,
        allow_none=True,
    )


class UpdateProjectSchema(Schema):
    name = fields.String(validate=validate.Length(min=1, max=255))
    description = fields.String(validate=validate.Length(max=2000), allow_none=True)


class PaginationSchema(Schema):
    page = fields.Integer(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Integer(load_default=20, validate=validate.Range(min=1, max=100))
