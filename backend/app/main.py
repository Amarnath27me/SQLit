import logging
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.config import settings
from app.api import query, problems, health, progress

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SQLit API",
    description="Backend API for SQLit — SQL practice platform",
    version="0.1.0",
    redirect_slashes=False,
)

# CORS — restrict to configured origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
    max_age=600,  # Cache preflight for 10 minutes
)


# Request logging middleware (added after CORS so it executes first)
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = (time.perf_counter() - start) * 1000
        logger.info("%s %s → %d (%.0fms)", request.method, request.url.path, response.status_code, elapsed)
        return response


app.add_middleware(RequestLoggingMiddleware)

# Routes
app.include_router(health.router, tags=["health"])
app.include_router(query.router, prefix="/api/query", tags=["query"])
app.include_router(problems.router, prefix="/api/problems", tags=["problems"])
app.include_router(progress.router, prefix="/api/progress", tags=["progress"])

logger.info("SQLit API ready — CORS origins: %s", settings.cors_origins_list)
