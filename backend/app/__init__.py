from flask import Flask, jsonify

from app.config import Config
from app.extensions import db, jwt, migrate
from app.routes.auth_routes import auth_bp
from app.routes.project_routes import project_bp
from app.routes.task_routes import task_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.models.project import Project  # noqa: F401
    from app.models.task import Task  # noqa: F401
    from app.models.user import User  # noqa: F401

    app.register_blueprint(auth_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(task_bp)

    @app.get("/health")
    def health_check():
        return jsonify({"status": "ok"})

    @app.errorhandler(404)
    def handle_not_found(_):
        return jsonify({"error": "Resource not found."}), 404

    @app.errorhandler(500)
    def handle_internal_error(_):
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred."}), 500

    return app
