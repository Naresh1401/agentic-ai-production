# Notes — Docker & CI/CD

## Why Docker
"Works on my machine" → "works everywhere". The image pins Python, deps, and
config so dev == CI == prod.

## Build context & caching
- Order matters: copy `requirements.txt` and install before copying source, so
  code changes don't bust the dependency layer.
- `.dockerignore` keeps the context small and builds fast.

## Image size
- Use `-slim`; consider `distroless` for runtime.
- Multi-stage: compilers/build deps stay out of the final image.
- Target < 300 MB for a FastAPI service.

## Security
- Run as a non-root user.
- Don't bake secrets into layers (they persist in history) — inject at runtime.
- Scan images (Trivy/Grype) in CI.

## CI/CD with GitHub Actions
- Trigger on `push`/`pull_request`.
- Jobs: lint → test → eval gate → build → deploy (deploy only on `main`).
- Store cloud/registry creds in repo **Secrets**; prefer OIDC over static keys.
- Tag images with `${{ github.sha }}` for traceability and rollback.

## Eval gate = quality CI
Wire Module 2's `run_eval.py` to exit non-zero below a threshold, then run it as
a required check. Now prompt/model changes can't silently regress.

## Rollback
Because images are tagged by SHA, rollback = redeploy the previous tag. Keep the
last few tags around.
