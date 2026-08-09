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

## ⚡ Quickstart
```bash
# 1. Create a virtual environment
python3 -m venv .venv && source .venv/bin/activate

# 2. Install shared dependencies
pip install -r requirements.txt

# 3. Copy env template and add your keys
cp .env.example .env

# 4. Run the module 1 API
uvicorn 01-fastapi-deployment.app.main:app --reload
```

## 🧭 How to use this repo
1. Read the module `README.md` and `notes.md`.
2. Run the code, break it, fix it.
3. Complete the exercises at the bottom of each module.
4. Track progress in [ROADMAP.md](ROADMAP.md) by checking off boxes.

## 📌 Progress tracker
Keep a short log in [PROGRESS.md](PROGRESS.md) — one line per session. Reviewing it weekly compounds fast.

---
Built as an ongoing learning journey. Contributions to your future self welcome. 🙌
