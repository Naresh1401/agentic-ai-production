# Agentic AI — Production & Advanced Skills 🚀

A hands-on, from-scratch-to-pro learning repo for **shipping real agentic systems**.
Each module is self-contained: read the notes, run the code, do the exercises, check yourself against the "Definition of done".

> Philosophy: build the *smallest real thing* that works end-to-end, then make it observable, safe, cheap, and fast.

## 🎯 What you'll be able to do
- Serve an LLM agent behind a production **FastAPI** API
- Measure quality with **evals** instead of vibes
- Add **guardrails** so agents fail safely
- **Trace** every request to debug and improve
- Deploy to **AWS / GCP / Azure** with **Docker** and **CI/CD**
- Cut **cost & latency** without hurting quality

## 🗺️ Learning path
Follow the modules in order. See [ROADMAP.md](ROADMAP.md) for the full plan, checklists, and resources.

| # | Module | Outcome |
|---|--------|---------|
| 1 | [FastAPI / Deployment](01-fastapi-deployment/) | Agent behind a real HTTP API |
| 2 | [Evaluation & Evals](02-evaluation-evals/) | Automated quality scoring |
| 3 | [Agent Safety & Guardrails](03-agent-safety-guardrails/) | Safe inputs/outputs & tool limits |
| 4 | [Observability & Tracing](04-observability-tracing/) | See inside every request |
| 5 | [Cloud (AWS/GCP/Azure)](05-cloud-aws-gcp-azure/) | Deploy to a managed runtime |
| 6 | [Docker & CI/CD](06-docker-cicd/) | Reproducible builds + auto tests/deploy |
| 7 | [Cost & Latency Optimization](07-cost-latency-optimization/) | Faster, cheaper, same quality |
| ★ | [Capstone Project](projects/) | Ship all of the above together |

## ⚡ Quickstart (one command each)
```bash
# 1. Get the repo
git clone https://github.com/Naresh1401/agentic-ai-production.git
cd agentic-ai-production

# 2. Set up everything (venv + deps + .env)
make setup

# 3. Run the API (works in mock mode without any API key)
make run
```

Prefer manual steps? Everything `make` does, by hand:
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --app-dir 01-fastapi-deployment
```

> Requires **Python 3.10+** (3.12 recommended). The service runs without any API
> key in **mock mode**, so every command works out of the box. Add keys to `.env`
> later to hit real models.

### Handy commands
| Command | What it does |
|---------|--------------|
| `make setup` | Create venv, install deps, create `.env` |
| `make run` | Start the agent API with hot reload |
| `make test` | Run the unit tests |
| `make eval` | Run the eval quality gate |
| `make demos` | Run all standalone learning demos |
| `make check` | Lint + test + eval (same as CI) |
| `make docker-build` | Build the production container |
| `make help` | List every target |

## 🧭 Guided walkthrough
Do the modules in order — each is ~30–60 min and ends with a working capability.

1. **[FastAPI / Deployment](01-fastapi-deployment/)** — `make run`, then `curl localhost:8000/health` and `POST /chat`.
2. **[Evaluation & Evals](02-evaluation-evals/)** — `make eval` to score the agent.
3. **[Agent Safety & Guardrails](03-agent-safety-guardrails/)** — `make test` (guardrail tests) + read the threat model.
4. **[Observability & Tracing](04-observability-tracing/)** — `python 04-observability-tracing/tracing.py` to see a trace.
5. **[Cloud (AWS/GCP/Azure)](05-cloud-aws-gcp-azure/)** — read the [environments](05-cloud-aws-gcp-azure/environments/) + [Azure](05-cloud-aws-gcp-azure/azure/README.md)/[GCP](05-cloud-aws-gcp-azure/gcp/README.md) guides.
6. **[Docker & CI/CD](06-docker-cicd/)** — `make docker-build`, then review the CI pipeline.
7. **[Cost & Latency](07-cost-latency-optimization/)** — `python 07-cost-latency-optimization/compare.py` for before/after.
8. **[Capstone](projects/)** — combine everything into one deployed agent.

Read each module's `README.md` (concepts + exercises) and `notes.md` (deep dive)
as you go, and check off boxes in [ROADMAP.md](ROADMAP.md).

## 📌 Progress tracker
Keep a short log in [PROGRESS.md](PROGRESS.md) — one line per session. Reviewing it weekly compounds fast.

---
Built as an ongoing learning journey. Contributions to your future self welcome. 🙌

