"""Standardized JSON response helpers."""

from flask import jsonify


def error_response(message: str, status_code: int = 400, errors: dict | None = None):
    """Return an error JSON response."""
    body = {"error": message}
    if errors:
        body["errors"] = errors
    return jsonify(body), status_code
