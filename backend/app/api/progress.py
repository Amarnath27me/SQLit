"""User progress API — tracks XP, level, streak, and solved problems.

Persists to PostgreSQL (sandbox database) so progress survives redeploys.
Falls back to in-memory storage if DB is unavailable.
"""

from __future__ import annotations

import logging
from datetime import date, datetime, timezone
from typing import Any

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel

from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

XP_PER_LEVEL = 100


def _compute_level(xp: int) -> int:
    return xp // XP_PER_LEVEL + 1


# ---------------------------------------------------------------------------
# PostgreSQL persistence (using sandbox DB with psycopg2)
# ---------------------------------------------------------------------------

_db_initialized = False


def _get_db_conn():
    """Get a psycopg2 connection to the sandbox database."""
    import psycopg2
    return psycopg2.connect(settings.sandbox_database_url, connect_timeout=3)


def _ensure_tables():
    """Create progress tables if they don't exist."""
    global _db_initialized
    if _db_initialized:
        return True

    try:
        conn = _get_db_conn()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sqlit_users (
                id SERIAL PRIMARY KEY,
                auth0_sub VARCHAR(255) UNIQUE NOT NULL,
                email VARCHAR(255),
                display_name VARCHAR(255),
                xp INTEGER DEFAULT 0,
                streak INTEGER DEFAULT 0,
                last_solve_date DATE,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sqlit_solves (
                id SERIAL PRIMARY KEY,
                auth0_sub VARCHAR(255) NOT NULL,
                problem_id VARCHAR(100) NOT NULL,
                xp_earned INTEGER DEFAULT 0,
                solved_at TIMESTAMP DEFAULT NOW(),
                UNIQUE(auth0_sub, problem_id)
            )
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_solves_sub
            ON sqlit_solves(auth0_sub)
        """)
        conn.commit()
        cur.close()
        conn.close()
        _db_initialized = True
        logger.info("Progress tables ready")
        return True
    except Exception as e:
        logger.warning("Could not initialize progress tables: %s", e)
        return False


def _load_user_progress(sub: str) -> dict[str, Any] | None:
    """Load user progress from PostgreSQL."""
    try:
        if not _ensure_tables():
            return None
        conn = _get_db_conn()
        cur = conn.cursor()

        # Get user record
        cur.execute(
            "SELECT xp, streak, last_solve_date FROM sqlit_users WHERE auth0_sub = %s",
            (sub,),
        )
        user_row = cur.fetchone()

        if not user_row:
            cur.close()
            conn.close()
            return {"xp": 0, "streak": 0, "last_solve_date": None, "solved": []}

        xp, streak, last_solve_date = user_row

        # Get solved problems
        cur.execute(
            "SELECT problem_id, xp_earned, solved_at FROM sqlit_solves WHERE auth0_sub = %s ORDER BY solved_at",
            (sub,),
        )
        solves = [
            {
                "problem_id": row[0],
                "xp_earned": row[1],
                "solved_at": row[2].isoformat() if row[2] else "",
            }
            for row in cur.fetchall()
        ]

        cur.close()
        conn.close()

        return {
            "xp": xp,
            "streak": streak,
            "last_solve_date": last_solve_date.isoformat() if last_solve_date else None,
            "solved": solves,
        }
    except Exception as e:
        logger.warning("Failed to load progress for %s: %s", sub, e)
        return None


def _save_solve(sub: str, problem_id: str, xp_earned: int) -> dict[str, Any] | None:
    """Record a solve and update user progress in PostgreSQL."""
    try:
        if not _ensure_tables():
            return None
        conn = _get_db_conn()
        cur = conn.cursor()

        today = date.today()
        now = datetime.now(timezone.utc)

        # Upsert user
        cur.execute(
            """
            INSERT INTO sqlit_users (auth0_sub, xp, streak, last_solve_date)
            VALUES (%s, 0, 0, NULL)
            ON CONFLICT (auth0_sub) DO NOTHING
            """,
            (sub,),
        )

        # Get current user state
        cur.execute(
            "SELECT xp, streak, last_solve_date FROM sqlit_users WHERE auth0_sub = %s",
            (sub,),
        )
        xp, streak, last_solve_date = cur.fetchone()

        # Update streak
        if last_solve_date is None:
            streak = 1
        elif last_solve_date == today:
            pass  # same day
        elif (today - last_solve_date).days == 1:
            streak += 1
        else:
            streak = 1

        # Update XP
        new_xp = xp + xp_earned

        # Save user updates
        cur.execute(
            """
            UPDATE sqlit_users
            SET xp = %s, streak = %s, last_solve_date = %s
            WHERE auth0_sub = %s
            """,
            (new_xp, streak, today, sub),
        )

        # Insert solve (ignore if already solved)
        cur.execute(
            """
            INSERT INTO sqlit_solves (auth0_sub, problem_id, xp_earned, solved_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (auth0_sub, problem_id) DO NOTHING
            """,
            (sub, problem_id, xp_earned, now),
        )

        conn.commit()

        # Load updated solves
        cur.execute(
            "SELECT problem_id, xp_earned, solved_at FROM sqlit_solves WHERE auth0_sub = %s ORDER BY solved_at",
            (sub,),
        )
        solves = [
            {
                "problem_id": row[0],
                "xp_earned": row[1],
                "solved_at": row[2].isoformat() if row[2] else "",
            }
            for row in cur.fetchall()
        ]

        cur.close()
        conn.close()

        return {"xp": new_xp, "streak": streak, "solved": solves}
    except Exception as e:
        logger.warning("Failed to save solve for %s: %s", sub, e)
        return None


# ---------------------------------------------------------------------------
# In-memory fallback (when DB is unavailable)
# ---------------------------------------------------------------------------

_user_progress: dict[str, dict[str, Any]] = {}


def _ensure_user_mem(sub: str) -> dict[str, Any]:
    if sub not in _user_progress:
        _user_progress[sub] = {
            "xp": 0,
            "streak": 0,
            "last_solve_date": None,
            "solved": [],
        }
    return _user_progress[sub]


# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------


class SolveRequest(BaseModel):
    problem_id: str
    xp_earned: int


class SolvedEntry(BaseModel):
    problem_id: str
    xp_earned: int
    solved_at: str


class ProgressResponse(BaseModel):
    xp: int
    level: int
    streak: int
    solved: list[SolvedEntry]


class StatsResponse(BaseModel):
    xp: int
    level: int
    streak: int
    total_solved: int
    xp_to_next_level: int


# ---------------------------------------------------------------------------
# Endpoints — use X-User-Sub header (set by Next.js proxy from Auth0 session)
# ---------------------------------------------------------------------------


def _get_user_sub(x_user_sub: str | None = Header(None)) -> str:
    if not x_user_sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    return x_user_sub


@router.get("", response_model=ProgressResponse)
@router.get("/", response_model=ProgressResponse)
async def get_progress(x_user_sub: str | None = Header(None)):
    """Return the authenticated user's progress."""
    sub = _get_user_sub(x_user_sub)

    # Try DB first
    record = _load_user_progress(sub)
    if record is None:
        record = _ensure_user_mem(sub)

    return ProgressResponse(
        xp=record["xp"],
        level=_compute_level(record["xp"]),
        streak=record["streak"],
        solved=[SolvedEntry(**s) for s in record["solved"]],
    )


@router.post("/solve", response_model=ProgressResponse, status_code=status.HTTP_200_OK)
async def record_solve(body: SolveRequest, x_user_sub: str | None = Header(None)):
    """Record that the user solved a problem, awarding XP and updating streak."""
    sub = _get_user_sub(x_user_sub)

    if body.xp_earned < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="xp_earned must be non-negative",
        )

    # Try DB first
    result = _save_solve(sub, body.problem_id, body.xp_earned)
    if result is not None:
        return ProgressResponse(
            xp=result["xp"],
            level=_compute_level(result["xp"]),
            streak=result["streak"],
            solved=[SolvedEntry(**s) for s in result["solved"]],
        )

    # Fallback to in-memory
    record = _ensure_user_mem(sub)
    today = date.today()

    if record["last_solve_date"] is None:
        record["streak"] = 1
    elif record["last_solve_date"] == today.isoformat():
        pass
    else:
        last = record["last_solve_date"]
        if isinstance(last, str):
            last = date.fromisoformat(last)
        if (today - last).days == 1:
            record["streak"] += 1
        elif (today - last).days > 1:
            record["streak"] = 1

    record["last_solve_date"] = today.isoformat()
    record["xp"] += body.xp_earned

    already_solved = any(s["problem_id"] == body.problem_id for s in record["solved"])
    if not already_solved:
        record["solved"].append(
            {
                "problem_id": body.problem_id,
                "xp_earned": body.xp_earned,
                "solved_at": datetime.now(timezone.utc).isoformat(),
            }
        )

    return ProgressResponse(
        xp=record["xp"],
        level=_compute_level(record["xp"]),
        streak=record["streak"],
        solved=[SolvedEntry(**s) for s in record["solved"]],
    )


@router.get("/stats", response_model=StatsResponse)
async def get_stats(x_user_sub: str | None = Header(None)):
    """Return aggregated stats suitable for a profile page."""
    sub = _get_user_sub(x_user_sub)

    record = _load_user_progress(sub)
    if record is None:
        record = _ensure_user_mem(sub)

    xp = record["xp"]
    level = _compute_level(xp)
    xp_to_next = (level * XP_PER_LEVEL) - xp

    return StatsResponse(
        xp=xp,
        level=level,
        streak=record["streak"],
        total_solved=len(record["solved"]),
        xp_to_next_level=xp_to_next,
    )
