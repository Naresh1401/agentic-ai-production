"""Module 2 concern: evaluate the capstone agent end to end.

Runs the real agent over a labeled dataset and reports a pass rate. Exits
non-zero below EVAL_THRESHOLD so it works as a CI quality gate.
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

# Make the `support_agent` package importable when run directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from support_agent import agent  # noqa: E402

DATASET = Path(__file__).parent / "dataset.jsonl"
THRESHOLD = float(os.getenv("EVAL_THRESHOLD", "1.0"))


async def _run_case(case: dict) -> bool:
    try:
        result = await agent.answer(case["input"], session_id=None)
    except agent.GuardrailBlocked:
        return case["expected"] == "BLOCKED"
    return case["expected"].lower() in result["answer"].lower()


def main() -> None:
    cases = [json.loads(line) for line in DATASET.read_text().splitlines() if line.strip()]
    by_cat: dict[str, list[bool]] = defaultdict(list)
    passed = 0

    print(f"Running {len(cases)} cases\n" + "-" * 40)
    for case in cases:
        ok = asyncio.run(_run_case(case))
        passed += ok
        by_cat[case["category"]].append(ok)
        print(f"[{'PASS' if ok else 'FAIL'}] {case['id']:<16} {case['input'][:40]}")

    rate = passed / len(cases)
    print("-" * 40)
    print(f"Overall: {passed}/{len(cases)} = {rate:.0%}")
    for cat, results in sorted(by_cat.items()):
        print(f"  {cat:<10} {sum(results)}/{len(results)}")

    if rate < THRESHOLD:
        print(f"\nFAIL: {rate:.0%} below threshold {THRESHOLD:.0%}")
        sys.exit(1)
    print(f"\nOK: {rate:.0%} meets threshold {THRESHOLD:.0%}")


if __name__ == "__main__":
    main()
