# Notes — Evaluation & Evals

## The eval loop
1. Collect real inputs (logs are gold — see Module 4).
2. Label expected behavior (answer, or a rubric).
3. Score automatically; sample human review.
4. Gate changes: block merges that regress (Module 6).

## Build datasets from production
Your best eval set is real traffic. Pull failing/edge cases from traces and
add them so you never regress on the same bug twice.

## LLM-as-judge tips
- Give the judge a **rubric** and ask for a score + short reason.
- Use a **stronger** model to judge a weaker one.
- Bias check: judges favor verbose/first answers — randomize order, keep short.
- Validate the judge against human labels on a sample.

## RAG-specific metrics (Ragas)
- **Faithfulness** — is the answer grounded in retrieved context?
- **Answer relevancy** — does it address the question?
- **Context precision/recall** — did retrieval fetch the right chunks?

## Statistical hygiene
- Report confidence: small sets are noisy. Aim for ≥50 cases per category.
- Track pass rate over time, not a single run.
- Separate **held-out** test set from prompt-tuning set to avoid overfitting.

## CI integration
Run evals in CI and fail if `pass_rate < threshold`. Keep the set fast (<1 min)
by sampling; run the full suite nightly.
