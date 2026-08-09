# Module 4 — Observability & Tracing

**Goal:** see inside every request — each LLM call, tool call, token, dollar,
and millisecond.

## Why
Agents are non-deterministic and multi-step. When something goes wrong you need
the full trace, not just a status code. Observability also feeds evals (Module 2)
and cost/latency work (Module 7).

## The three pillars
- **Logs** — structured, per-request, with a correlation ID
- **Traces** — a tree of spans (request → LLM call → tool call → …)
- **Metrics** — counts, latencies, tokens, cost, error rates

## What's here
```
tracing.py   # OpenTelemetry-style spans + a mock LLM span, runs standalone
```

## Run it
```bash
python 04-observability-tracing/tracing.py
```
Prints a nested trace with durations and token/cost attributes.

## What to capture per LLM call
| Attribute | Why |
|-----------|-----|
| model, prompt/version | reproduce & compare |
| input/output tokens | cost & context budgeting |
| latency (ttft, total) | UX & SLOs |
| tool name + args + result | debug agent loops |
| session/user id (hashed) | group multi-turn |
| eval score (if any) | quality over time |

## Backends to explore
- **Langfuse** — LLM-native traces, prompts, evals
- **Arize Phoenix** — open-source tracing + eval
- **OpenTelemetry + Grafana/Jaeger** — vendor-neutral standard
- Provider dashboards for token/cost baselines

## Golden signals + SLOs
- Latency p50/p95/p99, error rate, throughput, saturation
- Define an SLO (e.g. "p95 < 3s, 99% success") and alert on burn.

## Exercises
1. Wrap Module 1's `/chat` handler in a span; add request-id logging.
2. Emit token + cost as span attributes.
3. Export to Langfuse or an OTLP collector.
4. Add a dashboard panel for p95 latency and $/1k requests.

## Definition of done
- [x] Every request produces one trace with nested spans
- [x] Tokens, cost, and latency are attributes on spans
- [x] Logs carry a request/correlation ID

> The service adds a request-ID + structured-log + latency middleware
> (`01-fastapi-deployment/app/middleware.py`) and exposes `/metrics`.
> It also ships OpenTelemetry wiring (`01-fastapi-deployment/app/tracing.py`):
> set `OTEL_EXPORTER_OTLP_ENDPOINT` to stream traces to a live backend
> (Langfuse / Phoenix / Tempo / any OTLP collector); without it, spans are no-ops.
