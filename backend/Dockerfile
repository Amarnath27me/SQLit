# ---------- Build stage ----------
FROM python:3.12-slim AS base

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# ---------- Runtime ----------
# Verify the app can import without errors (build-time check)
RUN python -c "from app.main import app; print('App imports OK')"

# Default port — Railway overrides via $PORT env var
ENV PORT=8001

# Start server
CMD ["sh", "-c", "echo Starting on port $PORT && uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1 --log-level info"]
