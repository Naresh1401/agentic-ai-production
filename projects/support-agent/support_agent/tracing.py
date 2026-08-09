"""Module 4 concern: OpenTelemetry tracing (no-op unless an OTLP endpoint is set)."""
from __future__ import annotations

import os

from opentelemetry import trace

tracer = trace.get_tracer("support-agent")
_configured = False


def setup_tracing(service_name: str = "support-agent") -> bool:
    global _configured
    if _configured or not os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"):
        return _configured
    try:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter,
        )
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
    except ImportError:
        return False
    provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    trace.set_tracer_provider(provider)
    _configured = True
    return True
