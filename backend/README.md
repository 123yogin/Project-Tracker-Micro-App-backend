# Project Tracker Backend (Flask)

Production-ready Flask REST backend for a Project Tracker micro-application.

## Tech Stack

- Python 3.11+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate (Alembic)
- Flask-JWT-Extended
- SQLite (`sqlite:///project_tracker.db`)

## Project Structure

```text
backend/
│
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models/
│   │   ├── user.py
│   │   ├── project.py
│   │   └── task.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── project_routes.py
│   │   └── task_routes.py
│   └── config.py
│
├── migrations/
├── run.py
├── requirements.txt
└── README.md
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Export Flask app entrypoint:

```bash
export FLASK_APP=run.py
```

4. Initialize and apply migrations:

```bash
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

5. Run server:

```bash
python run.py
```

## Authentication API

- `POST /api/auth/register`
- `POST /api/auth/login`

### Register payload

```json
{
  "email": "user@example.com",
  "password": "StrongPassword123"
}
```

### Login payload

```json
{
  "email": "user@example.com",
  "password": "StrongPassword123"
}
```

> Pass JWT token in `Authorization: Bearer <token>` for protected routes.

## Project API (JWT required)

- `POST /api/projects`
- `GET /api/projects`
- `GET /api/projects/<id>`
- `PUT /api/projects/<id>`
- `DELETE /api/projects/<id>`

## Task API (JWT required)

- `POST /api/tasks`
- `GET /api/tasks/<project_id>`
- `PUT /api/tasks/<id>`
- `DELETE /api/tasks/<id>`

## Notes

- Passwords are hashed with `werkzeug.security`.
- Endpoints enforce ownership so users can only access their own projects/tasks.
- Global JSON error handlers for 404 and 500 responses.
