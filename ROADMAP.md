# 🗺️ Roadmap: From Scratch to Pro

A phased plan. Don't rush — each phase builds a real, working capability. Check boxes as you go.

## Phase 0 — Foundations (warm-up)
- [ ] Python async basics (`async`/`await`, event loop)
- [ ] HTTP fundamentals (methods, status codes, JSON)
- [ ] What an "agent" is: LLM + tools + loop + memory
- [ ] Set up `.venv`, install `requirements.txt`, add API keys to `.env`

## Phase 1 — Serve it (FastAPI / Deployment)
- [ ] Build a `/chat` endpoint that calls an LLM
- [ ] Add request/response Pydantic models
- [ ] Stream tokens with Server-Sent Events
- [ ] Health checks + graceful shutdown
- [ ] **DoD:** `curl` your agent and get a streamed answer

## Phase 2 — Measure it (Evals)
- [ ] Build a small labeled dataset (JSONL)
- [ ] Write deterministic checks (exact/regex/JSON schema)
- [ ] Add an LLM-as-judge scorer
- [ ] Report pass rate + regressions between runs
- [ ] **DoD:** one command prints a score you trust

## Phase 3 — Make it safe (Guardrails)
- [ ] Input validation (PII, prompt injection, jailbreak patterns)
- [ ] Output validation (schema, toxicity, hallucination checks)
- [ ] Tool-use limits (allowlist, rate limits, timeouts)
- [ ] Fail-safe fallbacks
- [ ] **DoD:** malicious inputs get blocked, logged, and handled

## Phase 4 — See it (Observability & Tracing)
- [ ] Structured logging (JSON logs with request IDs)
- [ ] Distributed tracing (OpenTelemetry spans per step)
- [ ] Token/cost/latency metrics per request
- [ ] Wire to a backend (Langfuse / Phoenix / OTLP collector)
- [ ] **DoD:** open one trace and see every LLM + tool call

## Phase 5 — Ship it (Cloud + Docker + CI/CD)
- [ ] Containerize with a slim, multi-stage Dockerfile
- [ ] CI: lint + test + build on every push
- [ ] Deploy to one cloud runtime (Cloud Run / ECS / Container Apps)
- [ ] Secrets management + config per environment
- [ ] **DoD:** push to `main` → tests run → deploys automatically

## Phase 6 — Optimize it (Cost & Latency)
- [ ] Measure baseline p50/p95 latency and $/request
- [ ] Prompt caching + response caching
- [ ] Model routing (small model first, escalate)
- [ ] Batching, concurrency, and streaming
- [ ] **DoD:** measurable cost/latency drop with equal eval score

## ★ Capstone
- [ ] Combine every module into one deployed, observable, safe, evaluated agent
- [ ] Write a short architecture doc + demo

---

## 📚 Curated resources
- **FastAPI** — official docs, `fastapi.tiangolo.com`
- **Evals** — OpenAI Evals, Ragas, promptfoo, DeepEval
- **Guardrails** — Guardrails AI, NeMo Guardrails, Llama Guard
- **Observability** — OpenTelemetry, Langfuse, Arize Phoenix
- **Cloud** — Cloud Run, AWS ECS/Fargate, Azure Container Apps
- **Docker/CI** — Docker docs, GitHub Actions
- **Cost/Latency** — provider pricing pages, prompt caching guides

> Add links you find useful under each phase as you learn.
