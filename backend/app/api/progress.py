"""User progress API — tracks XP, level, streak, and solved problems.

Data is stored in an in-memory dict keyed by user ``sub`` (from JWT).
This will be replaced by a proper database later.
"""

from __future__ import annotations

import math
from datetime import date, datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.core.auth import require_auth

router = APIRouter()

# ---------------------------------------------------------------------------
# In-memory store  (keyed by user sub)
# ---------------------------------------------------------------------------

_user_progress: dict[str, dict[str, Any]] = {}

XP_PER_LEVEL = 100  # XP required to advance one level


def _ensure_user(sub: str) -> dict[str, Any]:
    """Return (and lazily initialise) the progress record for *sub*."""
    if sub not in _user_progress:
        _user_progress[sub] = {
            "xp": 0,
            "streak": 0,
            "last_solve_date": None,
            "solved": [],  # list of {problem_id, xp_earned, solved_at}
        }
    return _user_progress[sub]


def _compute_level(xp: int) -> int:
    return xp // XP_PER_LEVEL + 1


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
# Endpoints
# ---------------------------------------------------------------------------


@router.get("", response_model=ProgressResponse)
@router.get("/", response_model=ProgressResponse)
async def get_progress(user: dict[str, Any] = Depends(require_auth)):
    """Return the authenticated user's progress."""
    record = _ensure_user(user["sub"])
    return ProgressResponse(
        xp=record["xp"],
        level=_compute_level(record["xp"]),
        streak=record["streak"],
        solved=[SolvedEntry(**s) for s in record["solved"]],
    )


@router.post("/solve", response_model=ProgressResponse, status_code=status.HTTP_200_OK)
async def record_solve(body: SolveRequest, user: dict[str, Any] = Depends(require_auth)):
    """Record that the user solved a problem, awarding XP and updating streak."""
    if body.xp_earned < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="xp_earned must be non-negative",
        )

    record = _ensure_user(user["sub"])
    today = date.today()

    # Update streak
    if record["last_solve_date"] is None:
        record["streak"] = 1
    elif record["last_solve_date"] == today:
        pass  # same day — streak unchanged
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

    # Record the solve
    record["xp"] += body.xp_earned
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
async def get_stats(user: dict[str, Any] = Depends(require_auth)):
    """Return aggregated stats suitable for a profile page."""
    record = _ensure_user(user["sub"])
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
