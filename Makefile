# Agentic AI — one-command workflows.
# Usage: `make help` to list targets. Requires Python 3.10+ (picks 3.12/3.11 if present).

PY ?= $(shell command -v python3.12 || command -v python3.11 || command -v python3)
VENV := .venv
BIN := $(VENV)/bin

.DEFAULT_GOAL := help

.PHONY: help setup run test eval lint demos capstone docker-build clean

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

setup: ## Create venv, install deps, copy .env
	$(PY) -m venv $(VENV)
	$(BIN)/pip install -U pip
	$(BIN)/pip install -r requirements.txt
	@[ -f .env ] || cp .env.example .env
	@echo "\nReady. Next: 'make run' (API) or 'make test'. Edit .env to add keys."

run: ## Run the API locally (works in mock mode without keys)
	$(BIN)/uvicorn app.main:app --reload --app-dir 01-fastapi-deployment

test: ## Run unit tests (service + guardrails)
	$(BIN)/pytest 01-fastapi-deployment/ 02-evaluation-evals/ 03-agent-safety-guardrails/ 07-cost-latency-optimization/ 08-agent-architecture/ projects/support-agent/

eval: ## Run the eval quality gate
	$(BIN)/python 02-evaluation-evals/evals/run_eval.py

lint: ## Lint the codebase
	$(BIN)/ruff check .

demos: ## Run the standalone learning demos
	$(BIN)/python 04-observability-tracing/tracing.py
	$(BIN)/python 07-cost-latency-optimization/optimize.py
	$(BIN)/python 07-cost-latency-optimization/cache.py
	$(BIN)/python 07-cost-latency-optimization/router.py
	$(BIN)/python 07-cost-latency-optimization/compare.py
	$(BIN)/python 08-agent-architecture/agent_demo.py

check: lint test eval ## Lint + test + eval (what CI runs)

docker-build: ## Build the production container image
	docker build -t agentic-ai -f 06-docker-cicd/Dockerfile .

clean: ## Remove venv and caches
	rm -rf $(VENV) .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
