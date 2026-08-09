# Notes — Agent Architecture & Orchestration

## The loop is the agent
Every agent is a loop: **plan → act → observe → repeat**. The LLM plans and
picks an action; your code executes it (tool call, retrieval, or final answer)
and feeds the result back. Bound the loop with a max-step budget.

## Tool use / function calling
- Describe each tool with a name, description, and typed parameters.
- The model returns a tool name + arguments; you validate and execute.
- Return the tool result to the model so it can decide the next step.
- Keep tools small, idempotent, and least-privilege (Module 3).

## RAG (retrieval-augmented generation)
Pipeline: **chunk → embed → store → retrieve → rerank → generate**.
- Chunk documents sensibly (semantic or fixed-size with overlap).
- Embed chunks and the query; retrieve top-k by cosine similarity.
- Optionally rerank for precision; pass only the best chunks as context.
- Ground the answer in retrieved text and cite it (measure with Ragas, Module 2).

## Memory
- **Short-term**: the conversation history (Module 1 session store).
- **Long-term**: facts/preferences stored in a vector DB or database and
  retrieved when relevant. Summarize old turns to fit the context budget.

## Orchestration patterns (simplest first)
1. **Single agent + tools** — handles most use cases. Start here.
2. **Router / handoff** — a classifier routes to a specialized agent.
3. **Planner + workers** — one agent decomposes, workers execute subtasks.
4. **Multi-agent review/debate** — agents critique each other (expensive).

> Rule of thumb: add orchestration complexity only when evals prove it improves
> quality. Complexity costs latency, money, and reliability.

## When to use a framework
- **No framework**: full control, easiest to debug — great to learn and for
  simple agents.
- **LangGraph**: explicit graphs/state machines for complex, cyclic flows.
- **LlamaIndex**: batteries-included RAG + agents.
- **MCP**: a standard protocol for exposing tools/data to any agent/host.

## Common pitfalls
- Unbounded loops (no step limit) → runaway cost.
- Dumping everything into context instead of retrieving the right few chunks.
- Over-engineering with multi-agent setups before a single agent is solid.
- Tools with too much privilege or unvalidated arguments (see Module 3).
