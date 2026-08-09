# Notes — Observability & Tracing

## Trace = a tree of spans
One request is a root span; each LLM/tool/guard step is a child span with a
duration and attributes. This is exactly what OpenTelemetry models.

## OpenTelemetry in FastAPI (production wiring)
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter())  # reads OTEL_EXPORTER_OTLP_ENDPOINT
)
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("llm.chat") as span:
    span.set_attribute("model", model)
    span.set_attribute("input_tokens", usage.prompt_tokens)
```

## Structured logging
Log JSON with a `request_id` on every line so you can grep one request end to
end. Never log secrets or full PII (redact — Module 3).

## LLM-native tools
Langfuse / Phoenix understand prompts, tokens, cost, and let you attach eval
scores to traces — closing the loop between Modules 2 and 4.

## Metrics & SLOs
- Track p50/p95/p99 latency, error rate, tokens, and $/request.
- Set SLOs and alert on error-budget burn, not raw spikes.
- Separate **time-to-first-token** from **total latency** for streaming UX.

## Close the loop
Feed interesting traces (failures, slow, expensive) back into your eval set
(Module 2) and your guardrail patterns (Module 3).
