# Project Tracker — Full Stack

Production-ready full-stack Project Tracker micro-application.

## Architecture

| Layer | Tech |
|-------|------|
| **Frontend** | React 18, Vite 5, React Router 6 |
| **Backend** | Python 3.12, Flask 3, SQLAlchemy, Marshmallow |
| **Auth** | JWT (access + refresh tokens, revocation) |
| **Database** | SQLite (drop-in replaceable with PostgreSQL) |
| **Deployment** | Docker, Gunicorn, Nginx |

## Project Structure

```
├── docker-compose.yml
├── .gitignore
│
├── Project-Tracker-Micro-App-backend/backend/
│   ├── app/
│   │   ├── __init__.py          # App factory, error handlers, security headers
│   │   ├── config.py            # Env-based configuration
│   │   ├── constants.py         # Shared enums (task status/priority)
│   │   ├── extensions.py        # Flask extensions (DB, JWT, CORS, Limiter)
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── project.py
│   │   │   └── task.py
│   │   ├── schemas/             # Marshmallow validation schemas
│   │   │   ├── auth_schema.py
│   │   │   ├── project_schema.py
│   │   │   └── task_schema.py
│   │   ├── services/            # Business logic layer
│   │   │   ├── base.py          # Shared ownership and pagination helpers
│   │   │   ├── auth_service.py
│   │   │   ├── project_service.py
│   │   │   └── task_service.py
│   │   ├── routes/              # Thin API controllers
│   │   │   ├── auth_routes.py
│   │   │   ├── project_routes.py
│   │   │   └── task_routes.py
│   │   └── utils/               # Exceptions, logging, response helpers
│   │       ├── exceptions.py
│   │       ├── logging_config.py
│   │       └── responses.py
│   ├── migrations/              # Alembic migrations
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── .env.example
│   ├── gunicorn.conf.py
│   ├── wsgi.py
│   ├── run.py                   # Dev-only entry point
│   └── requirements.txt
│
└── Project-Tracker-Micro-App-frontend/frontend/
    ├── src/
    │   ├── api/axios.js         # Axios instance with interceptors
    │   ├── context/AuthContext.jsx
    │   ├── components/          # Reusable UI components
    │   ├── pages/               # Route-level pages
    │   └── styles/global.css
    ├── Dockerfile
    ├── .dockerignore
    ├── .env.example
    ├── nginx.conf
    ├── vite.config.js
    └── package.json
```

## Quick Start (Development)

### Backend

```bash
cd Project-Tracker-Micro-App-backend/backend
cp .env.example .env       # Fill in JWT_SECRET_KEY and SECRET_KEY
pip install -r requirements.txt
flask db upgrade
python run.py              # Starts on http://localhost:5001
```

### Frontend

```bash
cd Project-Tracker-Micro-App-frontend/frontend
cp .env.example .env
npm install
npm run dev                # Starts on http://localhost:5173
```

## Production (Docker)

```bash
# From project root
docker compose up --build -d
# Frontend: http://localhost:3000
# Backend API: http://localhost:5001
```

## API Endpoints

| Method | Endpoint | Auth | Rate Limit |
|--------|----------|------|------------|
| POST | `/api/auth/register` | — | 10/hour |
| POST | `/api/auth/login` | — | 5/minute |
| POST | `/api/auth/refresh` | Refresh Token | — |
| POST | `/api/auth/logout` | Bearer Token | — |
| GET | `/api/projects` | Bearer Token | 200/hour |
| POST | `/api/projects` | Bearer Token | 200/hour |
| GET | `/api/projects/:id` | Bearer Token | 200/hour |
| PUT | `/api/projects/:id` | Bearer Token | 200/hour |
| DELETE | `/api/projects/:id` | Bearer Token | 200/hour |
| POST | `/api/tasks` | Bearer Token | 200/hour |
| GET | `/api/tasks/:project_id` | Bearer Token | 200/hour |
| PUT | `/api/tasks/:id` | Bearer Token | 200/hour |
| DELETE | `/api/tasks/:id` | Bearer Token | 200/hour |
| GET | `/health` | — | — |

## Environment Variables

See `.env.example` files in backend and frontend directories.
