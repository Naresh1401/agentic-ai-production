# Module 7 — Cost & Latency Optimization

**Goal:** make the agent faster and cheaper *without* dropping eval score.

## Golden rule
**Measure → change one thing → re-measure (quality + cost + latency).** Never
optimize blind; always guard quality with Module 2 evals.

## What's here
```
optimize.py   # benchmark harness: latency percentiles + cost estimate
cache.py      # exact-match + naive semantic response cache
router.py     # small-model-first routing with escalation metric
compare.py    # before/after: cost & latency drop at equal eval score
```

## Run it
```bash
python 07-cost-latency-optimization/optimize.py
python 07-cost-latency-optimization/cache.py
python 07-cost-latency-optimization/router.py
python 07-cost-latency-optimization/compare.py
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

## 📚 References
- OpenAI latency optimization guide: https://platform.openai.com/docs/guides/latency-optimization
- OpenAI prompt caching: https://platform.openai.com/docs/guides/prompt-caching
- Anthropic prompt caching: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- OpenAI pricing: https://openai.com/api/pricing/
- Anthropic pricing: https://www.anthropic.com/pricing
- vLLM (fast self-hosted inference): https://docs.vllm.ai/

## Definition of done
- [x] Baseline p50/p95 latency + $/request recorded (`optimize.py`)
- [x] One optimization applied with before/after numbers (`cache.py`, `router.py`)
- [x] Eval score unchanged (quality preserved) — see `compare.py`

> `compare.py` shows the routed config cutting cost and latency while re-running
> the module 02 eval to confirm the pass rate is unchanged.
