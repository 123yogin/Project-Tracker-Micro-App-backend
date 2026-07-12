# Project Tracker — Backend

Flask REST API for a project & task tracking micro-app, built with a layered
architecture (routes → services → models). Serves the
[Project-Tracker-Micro-App-frontend](https://github.com/123yogin/Project-Tracker-Micro-App-frontend).

## Features

- **Auth** (registration/login)
- **Projects** and **tasks** with full CRUD
- **Comments** on tasks/projects
- **Activity feed** and **notifications**
- **Search** across resources
- Request validation via schemas, structured error handling and logging
- Alembic migrations; production Gunicorn config; Dockerfile

## Tech stack

- Python + Flask (Blueprints, service layer)
- SQLAlchemy + Alembic migrations
- Gunicorn (production WSGI), Docker

> The service lives in the `backend/` directory.

## Getting started

```bash
cd backend
python -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
flask db upgrade
python -m flask run          # or: gunicorn -c gunicorn.conf.py "app:create_app()"
```

## Project structure

```
backend/app/
├─ routes/     auth, project, task, comment, notification, search, user
├─ services/   auth, project, task, search, activity (business logic)
├─ models/     user, project, task, comment, activity, notification
├─ schemas/    request/response validation
└─ utils/      exceptions, responses, logging
backend/migrations/   Alembic
```
