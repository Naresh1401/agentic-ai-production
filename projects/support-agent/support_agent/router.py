"""Module 7 concern: route easy prompts to a small model, hard ones to a large one."""
from __future__ import annotations

from .config import get_settings

HARD_SIGNALS = ("compare", "explain why", "step by step", "analyze", "recommend")


class Router:
    def __init__(self) -> None:
        self.escalations = 0
        self.total = 0

    def choose(self, prompt: str) -> str:
        self.total += 1
        settings = get_settings()
        low = prompt.lower()
        hard = len(prompt) > 300 or any(s in low for s in HARD_SIGNALS)
        if hard:
            self.escalations += 1
            return settings.large_model
        return settings.small_model


router = Router()
