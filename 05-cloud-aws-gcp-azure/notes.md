# Notes — Cloud

## Mental model
Managed container runtimes (Cloud Run, App Runner, Container Apps) give you:
image in → autoscaled HTTPS service out. You bring a container that listens on
`$PORT`; they handle TLS, scaling, and rollout.

## Listen on $PORT
Cloud runtimes inject a `PORT` env var. Your server must bind to it:
```bash
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

## Statelessness
Instances are ephemeral and can scale to zero. Keep no local state — use a DB,
cache (Redis), or object store for sessions/memory.

## Secrets, not env literals
Map secret-manager entries to env vars at deploy time. Rotate without redeploys.

## Concurrency tuning
LLM calls are I/O-bound, so one instance can handle many concurrent requests.
Set per-instance concurrency high (e.g. 40–80) and let autoscaling add
instances under load. Watch memory.

## Cold starts
Scale-to-zero saves money but adds cold-start latency. For latency-sensitive
apps set `min-instances=1`.

## Pick one, then generalize
The concepts (identity, secrets, ingress, autoscaling, budgets) transfer across
clouds. Master one provider deeply before going multi-cloud.
