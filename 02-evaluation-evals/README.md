# Module 2 — Evaluation & Evals Frameworks

**Goal:** replace "it feels good" with a number you trust.

## Why
You cannot improve what you don't measure. Evals catch regressions before your
users do and make prompt/model changes safe.

## What's here
```
evals/
  dataset.jsonl   # labeled examples (input + expected)
  run_eval.py     # runs the agent over the dataset and scores it
  scorers.py      # deterministic + LLM-as-judge scorers
```

## Run it
```bash
python 02-evaluation-evals/evals/run_eval.py
```
Prints per-case results and an overall pass rate. Uses mock agent output if no
API key, so it runs anywhere.

## Types of evals
| Type | Example | Cost | Reliability |
|------|---------|------|-------------|
| Deterministic | exact match, regex, JSON schema valid | free | high |
| Reference-based | similarity to gold answer | low | medium |
| LLM-as-judge | "is this answer correct & safe?" | $$ | medium-high |
| Human review | expert grading | $$$ | highest |

Start deterministic, add judge for open-ended tasks, sample human review.

## Metrics that matter
- **Pass rate** overall and **per category** (find weak spots)
- **Regression delta** vs the previous run
- **Faithfulness / groundedness** for RAG
- **Cost & latency** per case (tie into Module 7)

## Frameworks to explore
- **promptfoo** — config-driven, great for CI
- **Ragas** — RAG-specific metrics
- **DeepEval** — pytest-style LLM assertions
- **OpenAI Evals** — registry of graders

## Exercises
1. Add 10 real examples from your domain to `dataset.jsonl`.
2. Add a JSON-schema scorer for a structured-output task.
3. Fail CI (Module 6) when pass rate drops below a threshold.
4. Add per-category breakdown to the report.

## Definition of done
- [x] One command runs the eval and prints a pass rate
- [x] Dataset has ≥10 labeled cases
- [x] At least one deterministic + one judge scorer

> The eval doubles as a CI gate: it exits non-zero when the pass rate is below
> `EVAL_THRESHOLD` (default 100%). A JSON-schema scorer (`matches_schema`) and a
> working `llm_judge` (with an offline fallback) live in `evals/scorers.py`.
