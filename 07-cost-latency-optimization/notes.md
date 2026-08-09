# Notes — Cost & Latency

## Instrument first
You can't optimize what Module 4 doesn't measure. Emit tokens, cost, ttft, and
total latency per request, then find the biggest contributor.

## Where latency hides
- **Time-to-first-token** dominates perceived latency → stream.
- Long **output** is often the real cost/latency driver → cap `max_tokens`.
- Serial tool/LLM steps add up → parallelize independent ones.
- Oversized **context** slows every call → retrieve less, summarize more.

## Caching strategies
- **Prompt caching**: keep a stable prefix (system prompt, docs) so providers
  can cache it — big savings on repeated context.
- **Exact response cache**: hash inputs → store outputs (great for FAQs).
- **Semantic cache**: embed the query, reuse answers for near-duplicates.
- Always set a TTL and a way to invalidate.

## Model routing
Cheap/small model handles most traffic; escalate to a bigger model only when a
confidence check or classifier says it's hard. Track escalation rate.

## Guard quality
Every optimization must be re-run through Module 2 evals. A cheaper/faster
config that drops pass rate isn't a win.

## Quick wins checklist
- [x] Set `max_tokens`
- [x] Trim system prompt & few-shot
- [x] Stream responses
- [x] Add exact-match response cache
- [x] Try the next-smaller model behind an eval gate
