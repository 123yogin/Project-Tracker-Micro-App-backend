"""Authentication routes — register, login, refresh, logout."""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from marshmallow import ValidationError as MarshmallowValidationError

from app.extensions import limiter, revoke_token
from app.schemas.auth_schema import LoginSchema, RegisterSchema
from app.services.auth_service import AuthService
from app.utils.responses import error_response

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

_register_schema = RegisterSchema()
_login_schema = LoginSchema()


@auth_bp.post("/register")
@limiter.limit("10/hour")
def register():
    payload = request.get_json(silent=True) or {}

    try:
        data = _register_schema.load(payload)
    except MarshmallowValidationError as exc:
        return error_response("Validation failed.", 400, exc.messages)

    result = AuthService.register(data["email"], data["password"])
    return jsonify(result), 201


@auth_bp.post("/login")
@limiter.limit("5/minute")
def login():
    payload = request.get_json(silent=True) or {}

    try:
        data = _login_schema.load(payload)
    except MarshmallowValidationError as exc:
        return error_response("Validation failed.", 400, exc.messages)

    result = AuthService.login(data["email"], data["password"])
    return jsonify(result), 200


@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    """Issue a new access token using a valid refresh token."""
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    return jsonify({"access_token": new_access_token}), 200


@auth_bp.post("/logout")
@jwt_required()
def logout():
    """Revoke the current access token."""
    jti = get_jwt()["jti"]
    revoke_token(jti)
    return jsonify({"message": "Token revoked."}), 200
