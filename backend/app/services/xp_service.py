"""XP and streak calculation service."""

from datetime import datetime, timedelta

XP_REWARDS = {"easy": 10, "medium": 25, "hard": 50}

STREAK_MULTIPLIERS = [
    (30, 2.0),
    (7, 1.5),
    (3, 1.2),
]


def calculate_xp(difficulty: str, streak: int) -> int:
    """Calculate XP earned for solving a problem, including streak bonus."""
    base = XP_REWARDS.get(difficulty, 10)
    multiplier = 1.0
    for threshold, mult in STREAK_MULTIPLIERS:
        if streak >= threshold:
            multiplier = mult
            break
    return round(base * multiplier)


def calculate_level(total_xp: int) -> int:
    """Calculate level from total XP. Each level requires progressively more XP."""
    level = 1
    xp_needed = 100
    remaining = total_xp
    while remaining >= xp_needed:
        remaining -= xp_needed
        level += 1
        xp_needed = int(xp_needed * 1.3)
    return level


def update_streak(last_active: datetime | None, current: datetime | None = None) -> tuple[int, bool]:
    """Calculate if streak continues. Returns (streak_delta, streak_broken).

    streak_delta: +1 if new day, 0 if same day
    streak_broken: True if more than 1 day gap
    """
    if current is None:
        current = datetime.utcnow()

    if last_active is None:
        return 1, False

    diff = (current.date() - last_active.date()).days

    if diff == 0:
        return 0, False  # Same day
    elif diff == 1:
        return 1, False  # Consecutive day
    else:
        return 1, True  # Streak broken, restart at 1
