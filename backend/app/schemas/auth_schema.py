"""Authentication request validation schemas."""

from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    email = fields.Email(required=True, error_messages={"required": "Email is required."})
    password = fields.String(
        required=True,
        validate=validate.Length(min=8, max=128, error="Password must be 8–128 characters."),
        error_messages={"required": "Password is required."},
    )


class LoginSchema(Schema):
    email = fields.Email(required=True, error_messages={"required": "Email is required."})
    password = fields.String(
        required=True,
        validate=validate.Length(min=1),
        error_messages={"required": "Password is required."},
    )
