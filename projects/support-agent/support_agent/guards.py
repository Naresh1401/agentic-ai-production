"""Module 3 concern: input guardrails."""
from __future__ import annotations

import re
from dataclasses import dataclass

INJECTION_PATTERNS = [
    r"ignore (all|previous|above).*instructions",
    r"disregard (the )?system prompt",
    r"reveal your (system )?prompt",
]
PII_PATTERNS = {"email": r"[\w.+-]+@[\w-]+\.[\w.-]+"}


@dataclass
class GuardResult:
    allowed: bool
    reason: str = ""
    redacted: str | None = None


def guard_input(text: str, max_len: int = 4000) -> GuardResult:
    if len(text) > max_len:
        return GuardResult(allowed=False, reason="too_long")
    low = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, low):
            return GuardResult(allowed=False, reason=f"injection:{pattern}")
    redacted = text
    for name, pattern in PII_PATTERNS.items():
        redacted = re.sub(pattern, f"[REDACTED_{name.upper()}]", redacted)
    return GuardResult(allowed=True, redacted=redacted)
