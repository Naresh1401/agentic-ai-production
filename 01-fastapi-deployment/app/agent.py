"""A minimal agent: one LLM call plus a place to add a tool loop.

Falls back to a deterministic mock when no API key is configured, so the
service always runs during learning/dev.
"""
from __future__ import annotations

from collections.abc import AsyncIterator

from .config import get_settings

SYSTEM_PROMPT = (
    "You are a concise, helpful production assistant. "
    "Prefer short, correct answers."
)


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

    resp = await client.chat.completions.create(
        model=settings.default_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
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
