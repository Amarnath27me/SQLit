import logging

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
async def health_check():
    db_ok = False
    try:
        import psycopg2
        conn = psycopg2.connect(settings.sandbox_database_url, connect_timeout=2)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()
        db_ok = True
    except Exception as e:
        logger.warning("Health check DB probe failed: %s", e)

    return {
        "status": "ok" if db_ok else "degraded",
        "service": "sqlit-api",
        "database": "connected" if db_ok else "unavailable",
    }
