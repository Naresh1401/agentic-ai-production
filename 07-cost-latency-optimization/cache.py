"""Response caching examples: exact-match and a naive semantic cache.

Run: python 07-cost-latency-optimization/cache.py
"""
from __future__ import annotations

import time
from difflib import SequenceMatcher


class ExactCache:
    """Hash the exact input; reuse the stored answer. Great for FAQs."""

    def __init__(self, ttl_seconds: float = 300.0) -> None:
        self._store: dict[str, tuple[str, float]] = {}
        self._ttl = ttl_seconds
        self.hits = 0
        self.misses = 0

    def get(self, prompt: str) -> str | None:
        entry = self._store.get(prompt)
        if entry is None:
            self.misses += 1
            return None
        value, ts = entry
        if time.time() - ts > self._ttl:
            del self._store[prompt]
            self.misses += 1
            return None
        self.hits += 1
        return value

    def set(self, prompt: str, answer: str) -> None:
        self._store[prompt] = (answer, time.time())


class SemanticCache:
    """Reuse answers for *near-duplicate* prompts.

    Uses string similarity as a stand-in. In production, embed the prompt and
    compare vectors (cosine similarity) with a vector store.
    """

    def __init__(self, threshold: float = 0.85) -> None:
        self._items: list[tuple[str, str]] = []
        self._threshold = threshold
        self.hits = 0
        self.misses = 0

    def get(self, prompt: str) -> str | None:
        for stored_prompt, answer in self._items:
            if SequenceMatcher(None, prompt, stored_prompt).ratio() >= self._threshold:
                self.hits += 1
                return answer
        self.misses += 1
        return None

    def set(self, prompt: str, answer: str) -> None:
        self._items.append((prompt, answer))


def _demo() -> None:
    exact = ExactCache()
    exact.set("What is the capital of France?", "Paris")
    print("exact hit:", exact.get("What is the capital of France?"))
    print("exact miss:", exact.get("Capital of France?"))
    print(f"exact hit-rate: {exact.hits}/{exact.hits + exact.misses}")

    sem = SemanticCache(threshold=0.8)
    sem.set("What is the capital of France?", "Paris")
    print("semantic near-dup:", sem.get("what's the capital of France?"))
    print(f"semantic hit-rate: {sem.hits}/{sem.hits + sem.misses}")


if __name__ == "__main__":
    _demo()
