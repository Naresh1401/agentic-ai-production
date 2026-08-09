# Support Agent — Capstone Reference Implementation

A small, **complete** agentic system that combines every module in this repo:
a support assistant that answers FAQs via retrieval, does arithmetic with a
tool, is guarded, cached, routed, traced, evaluated, and container-ready.

## Which module each part embodies
| Concern | Module | Where |
|---------|--------|-------|
| HTTP service + streaming + session memory | 1 | [support_agent/main.py](support_agent/main.py), [support_agent/observability.py](support_agent/observability.py) |
| Eval suite + quality gate | 2 | [evals/](evals/run_eval.py) |
| Input guardrails | 3 | [support_agent/guards.py](support_agent/guards.py) |
| Tracing + metrics | 4 | [support_agent/tracing.py](support_agent/tracing.py), [support_agent/observability.py](support_agent/observability.py) |
| Cloud deploy | 5 | uses repo workflows |
| Docker + CI | 6 | [Dockerfile](Dockerfile) |
| Caching + model routing | 7 | [support_agent/cache.py](support_agent/cache.py), [support_agent/router.py](support_agent/router.py) |
| Agent loop + tools + RAG | 8 | [support_agent/agent.py](support_agent/agent.py), [support_agent/knowledge.py](support_agent/knowledge.py) |
| Infra as code + governance | 9 | uses repo Terraform/policy |

## Run it
```bash
# from repo root, with the shared venv active
uvicorn support_agent.main:app --reload --app-dir projects/support-agent

# try it
curl -s localhost:8000/health
curl -s -X POST localhost:8000/chat -H 'content-type: application/json' \
  -d '{"message":"How long do refunds take?","session_id":"u1"}'
curl -s -X POST localhost:8000/chat -H 'content-type: application/json' \
  -d '{"message":"What is 15 * 4?"}'
```

## Test + evaluate
```bash
pytest projects/support-agent/
python projects/support-agent/evals/run_eval.py     # 10/10 in mock mode
```

## Endpoints
- `GET /health` — liveness
- `POST /chat` — `{message, session_id?}` → `{answer, source, model, cached}`
- `POST /chat/stream` — token stream (SSE)
- `GET /chat/history/{session_id}` — session memory
- `GET /metrics` — request counts by source (rag/tool/llm/cache/blocked)

## How a request flows
See [ARCHITECTURE.md](ARCHITECTURE.md). In short: guardrails → cache →
route model → plan → act (calculator | RAG | LLM) → memory → response, with a
trace span around every step.

## Notes
- Runs in **mock mode** with no API key. Set `OPENAI_API_KEY` in `.env` to use a
  real model for the LLM-fallback path.
- Set `OTEL_EXPORTER_OTLP_ENDPOINT` to export traces to a real backend.
