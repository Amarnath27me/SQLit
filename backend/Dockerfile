# ---------- Build stage ----------
FROM python:3.12-slim AS base

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# ---------- Runtime ----------
# Railway injects $PORT dynamically — no need to EXPOSE a fixed port

# Remove Docker-level HEALTHCHECK — Railway uses its own HTTP healthcheck
# (Docker HEALTHCHECK can't read $PORT at build time, causing false failures)

# Start server — single worker for free tier (512MB), scale up via env var
CMD uvicorn app.main:app \
    --host 0.0.0.0 \
    --port ${PORT:-8001} \
    --workers ${WEB_WORKERS:-1} \
    --log-level info
