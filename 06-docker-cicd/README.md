# Module 6 — Docker & CI/CD

**Goal:** reproducible builds and an automated pipeline: push → lint → test →
eval → build image → deploy.

## What's here
```
Dockerfile          # slim, multi-stage image for the FastAPI service
.dockerignore
../.github/workflows/ci.yml   # GitHub Actions pipeline (repo root)
```

## Build & run locally
```bash
docker build -t agentic-ai -f 06-docker-cicd/Dockerfile .
docker run -p 8000:8000 --env-file .env agentic-ai
curl localhost:8000/health
```

## Dockerfile principles
- **Multi-stage** — build deps in one stage, copy only what's needed to run.
- **Slim base** — `python:3.12-slim`; avoid full images.
- **Layer caching** — copy `requirements.txt` and install *before* copying code.
- **Non-root user** — don't run as root.
- **`.dockerignore`** — keep `.venv`, `.git`, caches out of the build context.

## CI/CD pipeline stages
1. **Lint** — `ruff check`
2. **Test** — `pytest` (includes guardrail tests)
3. **Eval gate** — run Module 2 evals; fail if pass rate < threshold
4. **Build** — docker build (and push to a registry)
5. **Deploy** — to the cloud runtime (Module 5) on `main`

## Good CI hygiene
- Cache pip/deps for speed.
- Run on every PR; require green to merge.
- Keep secrets in GitHub Actions **secrets**, never in the repo.
- Tag images with the git SHA for traceable deploys + easy rollback.

## Exercises
1. Get the image under 300 MB.
2. Add the eval gate step and make it fail a PR intentionally.
3. Add a deploy job that runs only on `main`.
4. Add a rollback step/notes.

## Definition of done
- [ ] `docker run` serves the app locally
- [ ] CI runs lint + tests on every push
- [ ] Eval gate blocks regressions
- [ ] `main` auto-builds (and ideally deploys)
