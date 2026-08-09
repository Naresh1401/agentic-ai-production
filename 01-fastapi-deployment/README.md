# Module 1 — FastAPI / Deployment

**Goal:** put an LLM agent behind a real HTTP API you can call, stream, and deploy.

## Why this first
Nothing else matters until your agent is *reachable*. Evals, guardrails, tracing, and scaling all wrap around a running service. Build the service first.

## What's here
```
app/
  main.py     # FastAPI app: /health, /chat, /chat/stream
  agent.py    # Minimal agent (LLM call + tool loop stub)
  schemas.py  # Pydantic request/response models
  config.py   # Settings from env
```

## Run it
```bash
source ../.venv/bin/activate            # if not already
uvicorn app.main:app --reload --app-dir 01-fastapi-deployment
# from repo root, or cd into this folder and run: uvicorn app.main:app --reload
```

Test:
```bash
curl -s localhost:8000/health
curl -s -X POST localhost:8000/chat \
  -H 'content-type: application/json' \
  -d '{"message":"Explain what an AI agent is in one sentence."}'
```

Stream:
```bash
curl -N -X POST localhost:8000/chat/stream \
  -H 'content-type: application/json' \
  -d '{"message":"Count to five slowly."}'
```

> No API key? The agent falls back to an **echo/mock** mode so the API still runs.

## Core concepts
- **ASGI + async** — FastAPI is async; use `async def` and `await` for I/O.
- **Pydantic models** — validate inputs/outputs at the boundary.
- **Streaming** — return `StreamingResponse` / SSE for token-by-token UX.
- **Health checks** — `/health` for load balancers and orchestrators.
- **12-factor config** — everything from environment variables.

## Exercises
1. Add a `/chat/history` endpoint backed by an in-memory session store.
2. Add request timeouts and return `504` on model timeout.
3. Add API-key auth via a header dependency.
4. Add a `/metrics` endpoint (see Module 4).

## 📚 References
- FastAPI docs: https://fastapi.tiangolo.com/
- FastAPI deployment guide: https://fastapi.tiangolo.com/deployment/
- Uvicorn (ASGI server): https://www.uvicorn.org/
- Pydantic v2 docs: https://docs.pydantic.dev/latest/
- Starlette (underlying toolkit): https://www.starlette.io/
- MDN — Server-Sent Events: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
- The Twelve-Factor App: https://12factor.net/

## Definition of done
- [x] `curl /health` → `{"status":"ok"}`
- [x] `POST /chat` returns a model answer
- [x] `POST /chat/stream` streams tokens
- [x] App reads config from `.env`

> Exercises implemented: `/chat/history` (in-memory session store), request
> timeouts → `504`, API-key auth (`REQUIRE_AUTH`/`API_KEY`), and `/metrics`.
> Run the API tests: `pytest 01-fastapi-deployment/`

See [notes.md](notes.md) for deeper reference.
