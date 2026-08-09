"""OpenTelemetry tracing setup.

Exports spans to an OTLP backend (Langfuse / Phoenix / Grafana Tempo / any OTLP
collector) when `OTEL_EXPORTER_OTLP_ENDPOINT` is set. Without it, spans become
cheap no-ops so the service runs unchanged in dev/tests.
"""
from __future__ import annotations

import os

from opentelemetry import trace

# Works even before a provider is configured (returns no-op spans).
tracer = trace.get_tracer("agentic-ai")

_CONFIGURED = False


def setup_tracing(service_name: str = "agentic-ai") -> bool:
    """Configure the global tracer provider. Returns True if live export is on."""
    global _CONFIGURED
    if _CONFIGURED:
        return True
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if not endpoint:
        return False
    try:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter,
        )
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
    except ImportError:
        return False

    provider = TracerProvider(
        resource=Resource.create({"service.name": service_name})
    )
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    trace.set_tracer_provider(provider)
    _CONFIGURED = True
    return True
