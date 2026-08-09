"""Model routing: send easy prompts to a small model, escalate hard ones.

Run: python 07-cost-latency-optimization/router.py
"""
from __future__ import annotations

from dataclasses import dataclass, field

HARD_SIGNALS = ("prove", "derive", "step by step", "analy", "design", "architecture")


@dataclass
class Router:
    small_model: str = "gpt-4o-mini"
    large_model: str = "gpt-4o"
    length_threshold: int = 400
    escalations: int = 0
    total: int = 0
    _seen: list[str] = field(default_factory=list)

    def choose(self, prompt: str) -> str:
        """Return the model to use. Escalate on length or 'hard' keywords."""
        self.total += 1
        low = prompt.lower()
        hard = len(prompt) > self.length_threshold or any(s in low for s in HARD_SIGNALS)
        if hard:
            self.escalations += 1
            return self.large_model
        return self.small_model

    @property
    def escalation_rate(self) -> float:
        return self.escalations / self.total if self.total else 0.0


def _demo() -> None:
    router = Router()
    prompts = [
        "What is 2 + 2?",
        "Summarize this sentence.",
        "Derive the quadratic formula step by step and prove each step.",
        "Design a scalable architecture for a multi-tenant agent platform.",
    ]
    for p in prompts:
        print(f"{router.choose(p):<12} <- {p[:50]}")
    print(f"\nescalation rate: {router.escalation_rate:.0%} "
          f"({router.escalations}/{router.total})")


if __name__ == "__main__":
    _demo()
