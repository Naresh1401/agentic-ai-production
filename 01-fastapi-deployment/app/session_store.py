"""In-memory session history store.

Fine for dev/learning. In production use Redis or a database so history
survives restarts and works across multiple instances (see module 05 notes).
"""
from __future__ import annotations

from collections import defaultdict


class SessionStore:
    def __init__(self, max_messages: int = 100) -> None:
        self._data: dict[str, list[dict[str, str]]] = defaultdict(list)
        self._max = max_messages

    def add(self, session_id: str, role: str, content: str) -> None:
        history = self._data[session_id]
        history.append({"role": role, "content": content})
        # keep only the most recent messages
        del history[: max(0, len(history) - self._max)]

    def get(self, session_id: str) -> list[dict[str, str]]:
        return list(self._data.get(session_id, []))


store = SessionStore()
