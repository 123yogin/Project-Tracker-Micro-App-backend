"""Application factory."""

from flask import Flask, jsonify

from app.config import Config
from app.extensions import configure_jwt_blocklist, cors, db, jwt, limiter, migrate
from app.routes.auth_routes import auth_bp
from app.routes.project_routes import project_bp
from app.routes.task_routes import task_bp
from app.utils.exceptions import AppError, ValidationError
from app.utils.logging_config import setup_logging


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Validate critical config values
    Config.init_app(app)

    # ── Initialise extensions ───────────────────────────────────
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)

    # CORS — restricted to configured origins
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
        supports_credentials=False,
    )

    # JWT blocklist for logout / token revocation
    configure_jwt_blocklist(jwt)

    # Logging
    setup_logging(app)

    # ── Import models for Alembic ───────────────────────────────
    from app.models import Project, Task, User  # noqa: F401

    # ── Register blueprints ─────────────────────────────────────
    app.register_blueprint(auth_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(task_bp)

    # ── Health check ────────────────────────────────────────────
    @app.get("/health")
    def health_check():
        return jsonify({"status": "ok", "service": "project-tracker"})

    # ── Security headers ────────────────────────────────────────
    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        return response

    # ── Global error handlers ───────────────────────────────────
    @app.errorhandler(AppError)
    def handle_app_error(exc):
        body = {"error": exc.message}
        if isinstance(exc, ValidationError) and exc.errors:
            body["errors"] = exc.errors
        return jsonify(body), exc.status_code

    @app.errorhandler(404)
    def handle_not_found(_):
        return jsonify({"error": "Resource not found."}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(_):
        return jsonify({"error": "Method not allowed."}), 405

    @app.errorhandler(422)
    def handle_unprocessable(_):
        return jsonify({"error": "Unprocessable entity."}), 422

    @app.errorhandler(429)
    def handle_rate_limit(_):
        return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429

    @app.errorhandler(500)
    def handle_internal_error(_):
        db.session.rollback()
        app.logger.exception("Unhandled 500 error")
        return jsonify({"error": "An unexpected error occurred."}), 500

    return app
