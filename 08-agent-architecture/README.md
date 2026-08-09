# Module 8 — Agent Architecture & Orchestration

**Goal:** design the *agent itself* — the plan → act → observe loop, tool use,
retrieval (RAG), memory, and multi-agent orchestration.

## Why this matters
Modules 1–7 are the production wrapper (serve, evaluate, guard, observe, deploy,
optimize). **This module is the core** they wrap: how the agent actually decides
what to do. Read it early, then apply the production skills around it.

## What's here
```
agent_demo.py   # a dependency-free plan -> act -> answer loop with a tool + RAG
```

## Run it
```bash
python 08-agent-architecture/agent_demo.py
```
It routes each question to a **tool** (calculator), a **retriever** (RAG over a
tiny doc store), or a **direct answer**, and prints the reasoning trace. The
planner is deterministic here; in production you swap it for an LLM call.

## Core concepts
- **The agent loop** — plan the next step, act (call a tool / retrieve), observe
  the result, repeat until done or a step budget is hit.
- **Tool use / function calling** — expose typed tools; the model picks one and
  supplies arguments. Validate args (Module 3) before executing.
- **RAG (retrieval-augmented generation)** — fetch relevant context from a vector
  store and ground the answer in it (reduces hallucination).
- **Memory** — short-term (conversation history, Module 1) and long-term
  (vector/DB store of facts across sessions).
- **Orchestration patterns** — single agent + tools, router/handoff, planner +
  workers, and multi-agent debate/review. Prefer the *simplest* that works.

## Design principles (from the field)
- Start with a single well-prompted model + a couple of tools before reaching
  for a framework.
- Keep the loop **bounded** (max steps) and **observable** (trace every step).
- Make tools **idempotent** and **least-privilege** (Module 3).
- Add complexity (multi-agent, planners) only when evals (Module 2) show it helps.

## Exercises
1. Replace `plan()` with a real LLM call using function calling / structured output.
2. Swap the toy retriever for a real vector store (embeddings + cosine search).
3. Add a second tool (e.g. web search) and let the planner choose between tools.
4. Add long-term memory that persists facts across sessions.
5. Wire this agent into the Module 1 `/chat` endpoint.

## Definition of done
- [x] A bounded plan → act → observe loop that calls at least one tool
- [x] Retrieval grounds answers in fetched context
- [x] Every step is traced (ties into Module 4) — OpenTelemetry spans per step
- [x] The loop is evaluated (ties into Module 2) — see `test_agent.py`

## 📚 References
- Anthropic — Building effective agents: https://www.anthropic.com/research/building-effective-agents
- OpenAI — Agents guide & function calling: https://platform.openai.com/docs/guides/function-calling
- LangGraph (agent/graph orchestration): https://langchain-ai.github.io/langgraph/
- LlamaIndex (RAG + agents): https://docs.llamaindex.ai/
- ReAct: Reasoning + Acting (paper): https://arxiv.org/abs/2210.03629
- Retrieval-Augmented Generation (original paper): https://arxiv.org/abs/2005.11401
- Model Context Protocol (MCP): https://modelcontextprotocol.io/

See [notes.md](notes.md) for deeper reference.
