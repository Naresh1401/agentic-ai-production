"""Tiny in-process metrics registry exposed at /metrics.

Kept dependency-free for learning. In production, export to Prometheus or your
cloud monitoring backend (see module 04).
"""
from __future__ import annotations

import threading


class Metrics:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.requests_total = 0
        self.errors_total = 0
        self._latencies_ms: list[float] = []

    def observe_request(self, latency_ms: float, is_error: bool = False) -> None:
        with self._lock:
            self.requests_total += 1
            if is_error:
                self.errors_total += 1
            self._latencies_ms.append(latency_ms)
            # bound memory
            if len(self._latencies_ms) > 1000:
                self._latencies_ms = self._latencies_ms[-1000:]

    @staticmethod
    def _percentile(values: list[float], pct: float) -> float:
        if not values:
            return 0.0
        ordered = sorted(values)
        k = int(round((pct / 100) * (len(ordered) - 1)))
        return round(ordered[k], 2)

    def snapshot(self) -> dict[str, float]:
        with self._lock:
            latencies = list(self._latencies_ms)
        return {
            "requests_total": self.requests_total,
            "errors_total": self.errors_total,
            "latency_p50_ms": self._percentile(latencies, 50),
            "latency_p95_ms": self._percentile(latencies, 95),
        }


metrics = Metrics()
