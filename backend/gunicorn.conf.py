import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '5001')}"
backlog = 2048

# Worker processes
workers = int(os.environ.get("GUNICORN_WORKERS", "4"))
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Graceful shutdown
graceful_timeout = 30

# Logging
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("LOG_LEVEL", "info").lower()

# Process naming
proc_name = "project-tracker"

# Server mechanics
preload_app = True
max_requests = 1000
max_requests_jitter = 50
