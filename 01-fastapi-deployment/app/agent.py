"""A minimal agent: one LLM call plus a place to add a tool loop.

Falls back to a deterministic mock when no API key is configured, so the
service always runs during learning/dev.
"""
from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator

from .config import get_settings

SYSTEM_PROMPT = (
    "You are a concise, helpful production assistant. "
    "Prefer short, correct answers."
)

# Transient error class names worth retrying (matched by name so we don't hard
# depend on the openai package being importable).
_TRANSIENT = (
    "RateLimitError",
    "APITimeoutError",
    "APIConnectionError",
    "InternalServerError",
)


def _is_transient(exc: Exception) -> bool:
    return type(exc).__name__ in _TRANSIENT


async def _with_retries(coro_factory, max_retries: int):
    """Call an async factory, retrying transient errors with backoff."""
    attempt = 0
    while True:
        try:
            return await coro_factory()
        except Exception as exc:  # noqa: BLE001 - re-raised below if not transient
            if not _is_transient(exc) or attempt >= max_retries:
                raise
            await asyncio.sleep(0.5 * (2**attempt))  # 0.5s, 1s, 2s ...
            attempt += 1


async def _openai_client():
    """Lazily build an AsyncOpenAI client, or None if unavailable."""
    settings = get_settings()
    if not settings.openai_api_key:
        return None
    try:
        from openai import AsyncOpenAI
    except ImportError:
        return None
    return AsyncOpenAI(api_key=settings.openai_api_key)


async def run(message: str) -> tuple[str, bool]:
    """Return (reply, is_mock)."""
    settings = get_settings()
    client = await _openai_client()
    if client is None:
        return f"[mock] You said: {message}", True

    resp = await _with_retries(
        lambda: client.chat.completions.create(
            model=settings.default_model,
            max_tokens=settings.max_tokens,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
        ),
        settings.max_retries,
    )
    return resp.choices[0].message.content or "", False


async def stream(message: str) -> AsyncIterator[str]:
    """Yield reply chunks (tokens)."""
    settings = get_settings()
    client = await _openai_client()
    if client is None:
        for word in f"[mock] You said: {message}".split():
            yield word + " "
        return

    result = await client.chat.completions.create(
        model=settings.default_model,
        max_tokens=settings.max_tokens,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
        stream=True,
    )
    async for chunk in result:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
