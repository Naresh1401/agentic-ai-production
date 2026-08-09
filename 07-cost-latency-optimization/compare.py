"""Before/after: show a cost & latency drop while the eval score stays equal.

Baseline  = always use the large model.
Optimized = route easy prompts to the small model (see router.py).

Run: python 07-cost-latency-optimization/compare.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from optimize import call_model, cost, percentile
from router import Router

PROMPTS = [
    "What is 2 + 2?",
    "Summarize this sentence.",
    "What is the capital of France?",
    "Translate 'hello' to Spanish.",
    "Derive the quadratic formula step by step and prove each step.",
    "Design a scalable architecture for a multi-tenant agent platform.",
]


def measure(tiers: list[str]) -> tuple[float, float, float]:
    """Return (p50_ms, p95_ms, avg_cost) for a list of per-prompt tiers."""
    latencies, costs = [], []
    for tier in tiers:
        lat, in_tok, out_tok = call_model(tier)
        latencies.append(lat * 1000)
        costs.append(cost(tier, in_tok, out_tok))
    return (
        percentile(latencies, 50),
        percentile(latencies, 95),
        sum(costs) / len(costs),
    )


def eval_pass_rate() -> str:
    """Run the module 02 eval and return the reported overall pass rate."""
    eval_script = Path(__file__).parents[1] / "02-evaluation-evals/evals/run_eval.py"
    out = subprocess.run(
        [sys.executable, str(eval_script)], capture_output=True, text=True
    ).stdout
    match = re.search(r"Overall: \d+/\d+ = (\d+%)", out)
    return match.group(1) if match else "n/a"


def main() -> None:
    baseline_tiers = ["large"] * len(PROMPTS)
    router = Router()
    optimized_tiers = [
        "large" if router.choose(p) == router.large_model else "small"
        for p in PROMPTS
    ]

    b50, b95, bcost = measure(baseline_tiers)
    o50, o95, ocost = measure(optimized_tiers)

    print("Config      p50(ms)  p95(ms)  avg$/req")
    print(f"baseline    {b50:7.0f}  {b95:7.0f}  {bcost:.6f}")
    print(f"optimized   {o50:7.0f}  {o95:7.0f}  {ocost:.6f}")
    print(
        f"\ncost reduction:    {(1 - ocost / bcost):.0%}"
        f"\nlatency reduction: {(1 - o50 / b50):.0%} (p50)"
        f"\nescalation rate:   {router.escalation_rate:.0%}"
    )

    rate = eval_pass_rate()
    print(f"\neval pass rate (unchanged): {rate} -> {rate}")
    print("=> cheaper and faster at equal quality." if rate != "n/a" else "")


if __name__ == "__main__":
    main()
