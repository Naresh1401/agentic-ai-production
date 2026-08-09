"""Module 7 concern: exact-match response cache with TTL."""
from __future__ import annotations

import time

from .config import get_settings


class ResponseCache:
    def __init__(self) -> None:
        self._store: dict[str, tuple[str, float]] = {}
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> str | None:
        entry = self._store.get(key)
        if entry is None:
            self.misses += 1
            return None
        value, ts = entry
        if time.time() - ts > get_settings().cache_ttl_seconds:
            del self._store[key]
            self.misses += 1
            return None
        self.hits += 1
        return value

    def set(self, key: str, value: str) -> None:
        self._store[key] = (value, time.time())


response_cache = ResponseCache()
