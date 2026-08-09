"""Tiny benchmark harness: latency percentiles + cost estimate.

Uses a simulated model call so it runs anywhere. Replace `call_model` with a
real request to compare models/prompts fairly.
"""
from __future__ import annotations

import random
import statistics
import time

PRICE_PER_M = {
    "small": {"in": 0.15, "out": 0.60},
    "large": {"in": 2.50, "out": 10.00},
}


def call_model(tier: str) -> tuple[float, int, int]:
    """Simulate a call. Returns (latency_s, input_tokens, output_tokens)."""
    base = 0.15 if tier == "small" else 0.6
    latency = base + random.uniform(0, base)  # noqa: S311 (demo only)
    time.sleep(min(latency, 0.05))  # keep the demo fast
    return latency, 400, 120


def cost(tier: str, in_tok: int, out_tok: int) -> float:
    p = PRICE_PER_M[tier]
    return (in_tok * p["in"] + out_tok * p["out"]) / 1_000_000


def percentile(values: list[float], pct: float) -> float:
    values = sorted(values)
    k = int(round((pct / 100) * (len(values) - 1)))
    return values[k]


def benchmark(tier: str, n: int = 30) -> None:
    latencies, costs = [], []
    for _ in range(n):
        lat, in_tok, out_tok = call_model(tier)
        latencies.append(lat)
        costs.append(cost(tier, in_tok, out_tok))

    print(f"\nModel tier: {tier}  (n={n})")
    print(f"  p50 latency: {percentile(latencies, 50) * 1000:.0f} ms")
    print(f"  p95 latency: {percentile(latencies, 95) * 1000:.0f} ms")
    print(f"  avg cost/req: ${statistics.mean(costs):.6f}")
    print(f"  cost / 1k req: ${statistics.mean(costs) * 1000:.2f}")


if __name__ == "__main__":
    print("Baseline comparison — pick the cheapest tier that passes your evals.")
    benchmark("small")
    benchmark("large")
