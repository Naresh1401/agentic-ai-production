# Module 7 — Cost & Latency Optimization

**Goal:** make the agent faster and cheaper *without* dropping eval score.

## Golden rule
**Measure → change one thing → re-measure (quality + cost + latency).** Never
optimize blind; always guard quality with Module 2 evals.

## What's here
```
optimize.py   # tiny benchmark harness: latency percentiles + cost estimate
```

## Run it
```bash
python 07-cost-latency-optimization/optimize.py
```

## Levers (roughly high→low impact)
1. **Right-size the model** — use the smallest model that passes evals; route up
   only when needed (small-first, escalate on low confidence).
2. **Shrink the prompt** — trim system prompt, few-shot examples, and context.
   Tokens are latency *and* cost.
3. **Cache**
   - *Prompt caching* — reuse a static prefix (big system prompt / docs).
   - *Response caching* — identical inputs → cached answer (semantic cache for
     near-duplicates).
4. **Stream** — cut *perceived* latency (time-to-first-token).
5. **Parallelize** — fan out independent tool/LLM calls with `asyncio.gather`.
6. **Batch** — group requests where the API supports it.
7. **Limit output** — set `max_tokens`; long outputs cost and slow the most.
8. **Retrieve less** — fewer/better RAG chunks beat dumping everything.

## Cost math
```
cost = (input_tokens * price_in + output_tokens * price_out) / 1e6
```
Output tokens usually cost 3–5× input — watch verbosity.

## Latency budget (example SLO)
| Segment | Target |
|---------|--------|
| Guardrails + routing | < 50 ms |
| Retrieval | < 300 ms |
| LLM (time-to-first-token) | < 800 ms |
| Total p95 | < 3 s |

## Exercises
1. Benchmark p50/p95 for two models; keep the cheaper one if evals hold.
2. Add a response cache; measure hit rate and savings.
3. Parallelize two tool calls; compare total latency.
4. Cut the prompt by 30%; confirm eval score is unchanged.

## Definition of done
- [ ] Baseline p50/p95 latency + $/request recorded
- [ ] One optimization applied with before/after numbers
- [ ] Eval score unchanged (quality preserved)
