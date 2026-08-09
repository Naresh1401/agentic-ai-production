"""API-key authentication dependency."""
from __future__ import annotations

from fastapi import Header, HTTPException, status

from .config import get_settings


async def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """Reject requests without a valid API key when auth is enabled.

    Auth is off by default (dev). Enable it by setting REQUIRE_AUTH=true and
    API_KEY=<secret> in the environment.
    """
    settings = get_settings()
    if not settings.require_auth:
        return
    if not settings.api_key or x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or missing API key",
        )
