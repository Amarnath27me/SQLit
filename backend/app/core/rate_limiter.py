"""
Simple in-memory rate limiter.
Uses a sliding window per IP address.
"""

import time
from collections import defaultdict
from threading import Lock

from app.core.config import settings

_CLEANUP_INTERVAL = 100


class RateLimiter:
    def __init__(self, max_requests: int = 20, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)
        self._lock = Lock()
        self._request_count: int = 0

    def _cleanup_stale_entries(self) -> None:
        """Remove IP entries whose timestamps are all older than the window."""
        now = time.time()
        cutoff = now - self.window_seconds
        stale_keys = [
            key
            for key, timestamps in self._requests.items()
            if not timestamps or all(t <= cutoff for t in timestamps)
        ]
        for key in stale_keys:
            del self._requests[key]

    def is_allowed(self, key: str) -> bool:
        """Check if a request is allowed for the given key."""
        now = time.time()
        cutoff = now - self.window_seconds

        with self._lock:
            self._request_count += 1
            if self._request_count % _CLEANUP_INTERVAL == 0:
                self._cleanup_stale_entries()

            # Remove expired timestamps
            self._requests[key] = [
                t for t in self._requests[key] if t > cutoff
            ]

            if len(self._requests[key]) >= self.max_requests:
                return False

            self._requests[key].append(now)
            return True

    def remaining(self, key: str) -> int:
        """Get remaining requests for the given key."""
        now = time.time()
        cutoff = now - self.window_seconds

        with self._lock:
            self._requests[key] = [
                t for t in self._requests[key] if t > cutoff
            ]
            return max(0, self.max_requests - len(self._requests[key]))


# Global rate limiter instance
query_rate_limiter = RateLimiter(
    max_requests=settings.rate_limit_per_minute,
    window_seconds=60,
)
