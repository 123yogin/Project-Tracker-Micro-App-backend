"""Search routes."""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.search_service import SearchService

search_bp = Blueprint("search", __name__, url_prefix="/search")


@search_bp.route("/", methods=["GET"])
@jwt_required()
def search():
    """Search for projects and tasks."""
    user_id = get_jwt_identity()
    query = request.args.get("q", "")
    results = SearchService.search(user_id, query)
    return jsonify(results), 200
