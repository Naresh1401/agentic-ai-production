"""Tiny tracing demo — no external services required.

Shows the shape of spans/attributes you'd emit with OpenTelemetry or Langfuse.
Swap `Tracer` for the real OTEL SDK in production (see notes.md).
"""
from __future__ import annotations

import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field

# Rough price table ($ per 1M tokens) — update to your provider/model.
PRICE_PER_M = {"gpt-4o-mini": {"in": 0.15, "out": 0.60}}


@dataclass
class Span:
    name: str
    span_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    start: float = field(default_factory=time.perf_counter)
    duration_ms: float = 0.0
    attributes: dict = field(default_factory=dict)
    children: list["Span"] = field(default_factory=list)

    def print_tree(self, depth: int = 0) -> None:
        indent = "  " * depth
        attrs = " ".join(f"{k}={v}" for k, v in self.attributes.items())
        print(f"{indent}• {self.name} [{self.duration_ms:.1f}ms] {attrs}")
        for child in self.children:
            child.print_tree(depth + 1)


class Tracer:
    def __init__(self) -> None:
        self._stack: list[Span] = []
        self.root: Span | None = None

    @contextmanager
    def span(self, name: str, **attributes):
        s = Span(name=name, attributes=dict(attributes))
        if self._stack:
            self._stack[-1].children.append(s)
        else:
            self.root = s
        self._stack.append(s)
        try:
            yield s
        finally:
            s.duration_ms = (time.perf_counter() - s.start) * 1000
            self._stack.pop()


def cost(model: str, in_tok: int, out_tok: int) -> float:
    p = PRICE_PER_M.get(model, {"in": 0, "out": 0})
    return (in_tok * p["in"] + out_tok * p["out"]) / 1_000_000


def mock_llm_call(tracer: Tracer, model: str, in_tok: int, out_tok: int) -> None:
    with tracer.span("llm.chat", model=model) as s:
        time.sleep(0.05)  # simulate latency
        s.attributes.update(
            input_tokens=in_tok,
            output_tokens=out_tok,
            cost_usd=round(cost(model, in_tok, out_tok), 6),
        )


def main() -> None:
    tracer = Tracer()
    request_id = uuid.uuid4().hex[:8]
    with tracer.span("POST /chat", request_id=request_id) as root:
        with tracer.span("guardrails.input"):
            time.sleep(0.005)
        mock_llm_call(tracer, "gpt-4o-mini", in_tok=320, out_tok=110)
        with tracer.span("tool.search", query="weather paris"):
            time.sleep(0.02)
        mock_llm_call(tracer, "gpt-4o-mini", in_tok=450, out_tok=80)
        root.attributes["status"] = "ok"

    print("Trace:")
    tracer.root.print_tree()


if __name__ == "__main__":
    main()
