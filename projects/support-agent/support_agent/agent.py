"""The capstone agent: a bounded plan -> act -> observe loop that combines
guardrails, caching, model routing, RAG retrieval, tools, memory, and tracing.
"""
from __future__ import annotations

import re

from .cache import response_cache
from .config import get_settings
from .guards import guard_input
from .knowledge import retrieve
from .observability import memory, metrics
from .router import router
from .tracing import tracer


class GuardrailBlocked(Exception):
    """Raised when input fails a guardrail check."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


def _calculator(expression: str) -> str | None:
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expression):
        return None
    try:
        return str(eval(expression, {"__builtins__": {}}))  # noqa: S307 - sandboxed
    except Exception:
        return None


def _plan(question: str) -> tuple[str, str]:
    """Decide the next action. A real agent would use an LLM here."""
    if re.search(r"\d\s*[+\-*/]\s*\d", question):
        return "calculator", re.sub(r"[^0-9+\-*/(). ]", "", question).strip()
    doc, score = retrieve(question)
    if score > 0:
        return "retrieve", question
    return "answer", question


async def _llm_answer(question: str, model: str) -> str:
    settings = get_settings()
    if not settings.openai_api_key:
        return f"[mock:{model}] I don't have a specific answer, please contact support."
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    resp = await client.chat.completions.create(
        model=model,
        max_tokens=settings.max_tokens,
        messages=[
            {"role": "system", "content": "You are a concise support assistant."},
            {"role": "user", "content": question},
        ],
    )
    return resp.choices[0].message.content or ""


async def answer(question: str, session_id: str | None = None) -> dict:
    """Run the agent and return a structured result."""
    with tracer.start_as_current_span("agent.run") as span:
        settings = get_settings()

        if settings.enable_guardrails:
            with tracer.start_as_current_span("guardrails.input"):
                guard = guard_input(question)
            if not guard.allowed:
                metrics.record("blocked", blocked=True)
                raise GuardrailBlocked(guard.reason)
            question = guard.redacted or question

        cached = response_cache.get(question)
        if cached is not None:
            metrics.record("cache")
            span.set_attribute("source", "cache")
            return {"answer": cached, "source": "cache", "model": None, "cached": True}

        model = router.choose(question)
        span.set_attribute("model", model)

        with tracer.start_as_current_span("plan"):
            action, arg = _plan(question)

        if action == "calculator":
            with tracer.start_as_current_span("tool.calculator", attributes={"expr": arg}):
                result = _calculator(arg)
            source, reply = "tool:calculator", (result or "I couldn't compute that.")
        elif action == "retrieve":
            with tracer.start_as_current_span("tool.rag"):
                reply, _score = retrieve(question)
            source = "tool:rag"
        else:
            with tracer.start_as_current_span("llm.chat"):
                reply = await _llm_answer(question, model)
            source = "llm"

        response_cache.set(question, reply)
        metrics.record(source)
        span.set_attribute("source", source)

        if session_id:
            memory.add(session_id, "user", question)
            memory.add(session_id, "assistant", reply)

        return {"answer": reply, "source": source, "model": model, "cached": False}
