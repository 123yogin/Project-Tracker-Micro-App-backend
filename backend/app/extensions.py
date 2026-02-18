"""Flask extensions — initialised without app, bound in create_app()."""

from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per hour"],
    storage_uri="memory://",
)

# ── JWT token blocklist (in-memory; swap to Redis in production) ──
# Stores JTI (JWT ID) strings of revoked tokens.
_blocklist: set[str] = set()


def configure_jwt_blocklist(jwt_manager: JWTManager):
    """Wire up token revocation callbacks."""

    @jwt_manager.token_in_blocklist_loader
    def check_if_token_revoked(_jwt_header, jwt_payload):
        return jwt_payload["jti"] in _blocklist


def revoke_token(jti: str):
    """Add a token's JTI to the blocklist."""
    _blocklist.add(jti)
