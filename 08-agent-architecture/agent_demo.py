"""Minimal agent loop: plan -> act (tool or retrieve) -> answer.

Teaching skeleton with NO LLM dependency so it runs anywhere. In production,
replace `plan()` with an LLM call (function calling / structured output) that
chooses the next action, and swap the toy retriever for a real vector store.
"""
from __future__ import annotations

import re
from contextlib import contextmanager

try:  # optional: emit OpenTelemetry spans when the SDK is available
    from opentelemetry import trace as _otel

    _tracer = _otel.get_tracer("agent-demo")
except Exception:  # pragma: no cover - otel not installed
    _tracer = None


@contextmanager
def _span(name: str, **attributes):
    """Emit a span per agent step (no-op unless OpenTelemetry is configured)."""
    if _tracer is None:
        yield
        return
    with _tracer.start_as_current_span(name) as span:
        for key, value in attributes.items():
            span.set_attribute(key, value)
        yield


# --- Tools ---------------------------------------------------------------


def calculator(expression: str) -> str:
    """Evaluate a simple arithmetic expression in a locked-down namespace."""
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expression):
        return "unsupported expression"
    try:
        return str(eval(expression, {"__builtins__": {}}))  # noqa: S307 - sandboxed
    except Exception:
        return "error"


# Tiny knowledge base used by the retriever (stands in for a vector store).
DOCS = {
    "refund": "Refunds are processed within 5 business days to the original method.",
    "hours": "Support is available 9am-5pm on weekdays.",
    "shipping": "Standard shipping takes 3-5 business days.",
}


def retrieve(query: str) -> str:
    q = query.lower()
    for key, text in DOCS.items():
        if key in q:
            return text
    return "no relevant document found"


# --- Planner (an LLM would decide this in production) --------------------


def plan(question: str) -> tuple[str, str]:
    """Return (action, argument): 'calculator', 'retrieve', or 'answer'."""
    q = question.lower()
    if re.search(r"\d\s*[+\-*/]", question):
        expr = re.sub(r"[^0-9+\-*/(). ]", "", question)
        return "calculator", expr.strip()
    if any(k in q for k in DOCS):
        return "retrieve", question
    return "answer", question


# --- Agent loop ----------------------------------------------------------


def run_agent(question: str, max_steps: int = 3) -> str:
    trace: list[str] = []
    with _span("agent.run", question=question):
        for _ in range(max_steps):
            with _span("plan"):
                action, arg = plan(question)
            trace.append(f"plan -> {action}({arg!r})")
            if action == "calculator":
                with _span("tool.calculator", expression=arg):
                    result = calculator(arg)
                trace.append(f"tool calculator -> {result}")
                return _finalize(result, trace)
            if action == "retrieve":
                with _span("tool.retrieve", query=arg):
                    result = retrieve(arg)
                trace.append(f"retrieved -> {result}")
                return _finalize(result, trace)
            return _finalize(f"(direct answer to) {arg}", trace)
    return _finalize("gave up (step budget exhausted)", trace)


def _finalize(answer: str, trace: list[str]) -> str:
    print("  " + "\n  ".join(trace))
    return answer


if __name__ == "__main__":
    for q in ["What is 12 * (3 + 4)?", "What is your refund policy?", "Say hello"]:
        print(f"\nQ: {q}")
        print(f"A: {run_agent(q)}")
