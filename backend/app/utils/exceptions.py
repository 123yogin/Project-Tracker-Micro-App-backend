"""Custom application exceptions.

Each exception carries a message and HTTP status code.
The global error handler in __init__.py catches these and
returns a standardized JSON error response.
"""


class AppError(Exception):
    """Base application error."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ValidationError(AppError):
    """Input validation failure — 400."""

    def __init__(self, message: str = "Validation failed", errors: dict | None = None):
        super().__init__(message, status_code=400)
        self.errors = errors or {}


class AuthenticationError(AppError):
    """Authentication failure — 401."""

    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message, status_code=401)


class NotFoundError(AppError):
    """Resource not found — 404."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class ConflictError(AppError):
    """Resource conflict — 409."""

    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, status_code=409)
