# 🗺️ Roadmap: From Scratch to Pro

A phased plan. Don't rush — each phase builds a real, working capability. Check boxes as you go.

## Phase 0 — Foundations (warm-up)
- [ ] Python async basics (`async`/`await`, event loop)
- [ ] HTTP fundamentals (methods, status codes, JSON)
- [ ] What an "agent" is: LLM + tools + loop + memory
- [x] Set up `.venv`, install `requirements.txt`, add API keys to `.env`

## Phase 1 — Serve it (FastAPI / Deployment)
- [x] Build a `/chat` endpoint that calls an LLM
- [x] Add request/response Pydantic models
- [x] Stream tokens with Server-Sent Events
- [x] Health checks + graceful shutdown
- [x] **DoD:** `curl` your agent and get a streamed answer

## Phase 2 — Measure it (Evals)
- [x] Build a small labeled dataset (JSONL)
- [x] Write deterministic checks (exact/regex/JSON schema)
- [x] Add an LLM-as-judge scorer
- [x] Report pass rate + regressions between runs
- [x] **DoD:** one command prints a score you trust

## Phase 3 — Make it safe (Guardrails)
- [x] Input validation (PII, prompt injection, jailbreak patterns)
- [x] Output validation (schema, toxicity, hallucination checks)
- [x] Tool-use limits (allowlist, rate limits, timeouts)
- [x] Fail-safe fallbacks
- [x] **DoD:** malicious inputs get blocked, logged, and handled

## Phase 4 — See it (Observability & Tracing)
- [x] Structured logging (JSON logs with request IDs)
- [x] Distributed tracing (OpenTelemetry spans per step)
- [x] Token/cost/latency metrics per request
- [x] Wire to a backend (Langfuse / Phoenix / OTLP collector) — set `OTEL_EXPORTER_OTLP_ENDPOINT`
- [x] **DoD:** open one trace and see every LLM + tool call

## Phase 5 — Ship it (Cloud + Docker + CI/CD)
- [x] Containerize with a slim, multi-stage Dockerfile
- [x] CI: lint + test + build on every push
- [x] Define **dev / stage / prod / on-prem** environments (config, not code)
- [ ] Deploy to one cloud runtime (Cloud Run / ECS / Container Apps) — needs a live cloud account
- [x] Go deep on **Azure** (Container Apps, Key Vault, Entra ID) and **GCP**
      (Cloud Run, Secret Manager, IAM) — see `05-cloud-aws-gcp-azure/azure` and `/gcp`
- [x] Secrets management + config per environment
- [x] Promote one image dev → stage → prod (build-once pipeline in `.github/workflows/ci.yml`)
- [x] **DoD:** push to `main` → tests run → deploys automatically (pipeline in `.github/workflows/ci.yml`; needs GCP secrets configured)

## Phase 6 — Optimize it (Cost & Latency)
- [x] Measure baseline p50/p95 latency and $/request
- [x] Prompt caching + response caching
- [x] Model routing (small model first, escalate)
- [x] Batching, concurrency, and streaming
- [x] **DoD:** measurable cost/latency drop with equal eval score (`07-cost-latency-optimization/compare.py`)

## Phase 7 — Level up the agent core (Architecture & Orchestration)
- [ ] Build a bounded plan → act → observe loop
- [ ] Add tool use / function calling with validated arguments
- [ ] Add retrieval (RAG) to ground answers in fetched context
- [ ] Add short- and long-term memory
- [ ] Choose the simplest orchestration pattern that passes evals
- [ ] **DoD:** the agent uses a tool and grounded retrieval, fully traced

> Foundational — you can read `08-agent-architecture/` right after Phase 1.

## Phase 8 — Govern the platform (Infrastructure & Cloud Governance)
- [ ] Define infrastructure as code (Terraform) per environment
- [ ] Enforce standard labels/tags (variable validation + policy)
- [ ] Add policy-as-code checks (OPA/Conftest) in CI
- [ ] Least-privilege identity, keyless auth, remote locked state
- [ ] Budgets/quotas + scheduled drift detection
- [ ] **DoD:** a non-compliant change is blocked automatically

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
