"""JWT verification middleware for Auth0 RS256 tokens."""

from __future__ import annotations

import json
import time
from functools import lru_cache
from typing import Any

import httpx
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings

# Optional bearer — allows unauthenticated requests through
_bearer_scheme = HTTPBearer(auto_error=False)

# Required bearer — rejects requests without a token
_bearer_scheme_required = HTTPBearer(auto_error=True)


# ---------------------------------------------------------------------------
# JWKS helpers
# ---------------------------------------------------------------------------

_jwks_cache: dict[str, Any] | None = None
_jwks_cache_time: float = 0
_JWKS_CACHE_TTL = 86400  # 24 hours


async def _fetch_jwks() -> dict[str, Any]:
    """Fetch the JSON Web Key Set from Auth0 (cached for 24 hours)."""
    global _jwks_cache, _jwks_cache_time
    now = time.monotonic()
    if _jwks_cache is not None and (now - _jwks_cache_time) < _JWKS_CACHE_TTL:
        return _jwks_cache

    jwks_url = f"https://{settings.auth0_domain}/.well-known/jwks.json"
    async with httpx.AsyncClient() as client:
        resp = await client.get(jwks_url, timeout=10)
        resp.raise_for_status()
        _jwks_cache = resp.json()
        _jwks_cache_time = now
        return _jwks_cache


def _get_signing_key(jwks: dict[str, Any], kid: str) -> str:
    """Extract the RSA public key matching the given kid from JWKS."""
    for key in jwks.get("keys", []):
        if key["kid"] == kid:
            return jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to find matching signing key",
    )


# ---------------------------------------------------------------------------
# Token verification
# ---------------------------------------------------------------------------


async def _verify_token(token: str) -> dict[str, Any]:
    """Decode and verify an Auth0 JWT, returning the payload claims."""
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token header",
        )

    kid = unverified_header.get("kid")
    if kid is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token header missing kid",
        )

    jwks = await _fetch_jwks()
    public_key = _get_signing_key(jwks, kid)

    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=settings.auth0_algorithms_list,
            audience=settings.auth0_api_audience,
            issuer=f"https://{settings.auth0_domain}/",
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {exc}",
        )

    return payload


# ---------------------------------------------------------------------------
# FastAPI dependencies
# ---------------------------------------------------------------------------


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
) -> dict[str, Any] | None:
    """Return user claims if a valid token is present, otherwise ``None``.

    Use this for endpoints where authentication is *optional*.
    """
    if credentials is None:
        return None
    return await _verify_token(credentials.credentials)


async def require_auth(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme_required),
) -> dict[str, Any]:
    """Return user claims or raise 401.

    Use this for endpoints where authentication is *required*.
    """
    return await _verify_token(credentials.credentials)
