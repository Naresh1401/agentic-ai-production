"""Lightweight input guardrails used by the service.

Mirrors the teaching examples in module 03 so the service is self-contained.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

INJECTION_PATTERNS = [
    r"ignore (all|previous|above).*instructions",
    r"disregard (the )?system prompt",
    r"reveal your (system )?prompt",
    r"you are now",
    r"pretend to be",
]

PII_PATTERNS = {
    "email": r"[\w.+-]+@[\w-]+\.[\w.-]+",
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
}


@dataclass
class GuardResult:
    allowed: bool
    reason: str = ""
    redacted: str | None = None


def guard_input(text: str, max_len: int = 8000) -> GuardResult:
    if len(text) > max_len:
        return GuardResult(allowed=False, reason="too_long")
    low = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, low):
            return GuardResult(allowed=False, reason=f"injection:{pattern}")
    redacted = text
    found = []
    for name, pattern in PII_PATTERNS.items():
        if re.search(pattern, redacted):
            found.append(name)
            redacted = re.sub(pattern, f"[REDACTED_{name.upper()}]", redacted)
    return GuardResult(allowed=True, reason=",".join(found), redacted=redacted)
