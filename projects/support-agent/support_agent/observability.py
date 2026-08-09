"""Module 4 concern: in-process metrics; Module 1 concern: session memory."""
from __future__ import annotations

import threading
from collections import defaultdict


class Metrics:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.requests_total = 0
        self.blocked_total = 0
        self.by_source: dict[str, int] = defaultdict(int)

    def record(self, source: str, blocked: bool = False) -> None:
        with self._lock:
            self.requests_total += 1
            if blocked:
                self.blocked_total += 1
            else:
                self.by_source[source] += 1

    def snapshot(self) -> dict:
        with self._lock:
            return {
                "requests_total": self.requests_total,
                "blocked_total": self.blocked_total,
                "by_source": dict(self.by_source),
            }


class SessionMemory:
    def __init__(self, max_turns: int = 50) -> None:
        self._data: dict[str, list[dict[str, str]]] = defaultdict(list)
        self._max = max_turns

    def add(self, session_id: str, role: str, content: str) -> None:
        history = self._data[session_id]
        history.append({"role": role, "content": content})
        del history[: max(0, len(history) - self._max)]

    def get(self, session_id: str) -> list[dict[str, str]]:
        return list(self._data.get(session_id, []))


metrics = Metrics()
memory = SessionMemory()
