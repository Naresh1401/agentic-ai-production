# Notes — FastAPI / Deployment

## Mental model
An agent service is just a web service whose handler happens to call an LLM
(and maybe tools) before responding. Everything you know about good web
services still applies: validation, timeouts, retries, health checks, logging.

## Async & concurrency
- Use `async def` for handlers doing network I/O (LLM/tool calls).
- One slow blocking call blocks the event loop — never call sync blocking code
  directly; use `await`, `httpx.AsyncClient`, or `run_in_threadpool`.
- Uvicorn workers scale CPU; async scales I/O concurrency within a worker.

## Streaming (why it matters)
- Time-to-first-token dominates *perceived* latency.
- Server-Sent Events (SSE): `text/event-stream`, lines prefixed with `data: `.
- WebSockets when you need bidirectional/interactive control.

## Production checklist
- [x] `/health` (liveness) and `/ready` (readiness) endpoints
- [x] Request timeouts + upstream (model) timeouts
- [x] Retries with backoff on transient model errors (429/5xx)
- [x] Structured JSON logs with a request ID
- [x] Input size limits (see `max_length` on schema)
- [x] Graceful shutdown (drain in-flight requests)
- [x] CORS configured for your frontend only

## Deploy targets (preview of Module 5)
- Containerize (Module 6), then run on Cloud Run / ECS / Container Apps.
- Set env vars via the platform's secret manager, not in the image.

## Common pitfalls
- Blocking the event loop with a sync SDK call.
- No timeout → one hung model call ties up a worker.
- Returning raw model errors to clients (leak internals).
- Forgetting to flush/stream — buffering kills the streaming UX.
