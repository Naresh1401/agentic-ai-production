"""FastAPI entrypoint for the agent service.

Wires together: auth, input guardrails, request timeouts, session history,
metrics, and structured request logging.
"""
from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from . import agent
from .config import get_settings
from .guards import guard_input
from .metrics import metrics
from .middleware import ObservabilityMiddleware
from .schemas import (
    ChatRequest,
    ChatResponse,
    HistoryResponse,
    Message,
    MetricsResponse,
)
from .security import require_api_key
from .session_store import store
from .tracing import setup_tracing, tracer


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    setup_tracing()
    yield
    # shutdown: flush any buffered traces so nothing is lost on drain
    from opentelemetry import trace

    provider = trace.get_tracer_provider()
    if hasattr(provider, "shutdown"):
        provider.shutdown()


app = FastAPI(title="Agentic AI Service", version="0.1.0", lifespan=lifespan)
app.add_middleware(ObservabilityMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins_list,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok"}


@app.get("/ready")
async def ready() -> dict[str, str]:
    """Readiness probe — confirms config loads."""
    get_settings()
    return {"status": "ready"}


@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics() -> MetricsResponse:
    return MetricsResponse(**metrics.snapshot())


@app.post("/chat", response_model=ChatResponse, dependencies=[Depends(require_api_key)])
async def chat(req: ChatRequest) -> ChatResponse:
    settings = get_settings()

    if settings.enable_guardrails:
        guard = guard_input(req.message)
        if not guard.allowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"blocked by guardrails: {guard.reason}",
            )
        message = guard.redacted or req.message
    else:
        message = req.message

    try:
        with tracer.start_as_current_span("agent.run") as span:
            span.set_attribute("model", settings.default_model)
            reply, mock = await asyncio.wait_for(
                agent.run(message), timeout=settings.request_timeout_seconds
            )
            span.set_attribute("mock", mock)
    except asyncio.TimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="model request timed out",
        ) from exc

    if req.session_id:
        store.add(req.session_id, "user", message)
        store.add(req.session_id, "assistant", reply)

    return ChatResponse(reply=reply, model=settings.default_model, mock=mock)


@app.post("/chat/stream", dependencies=[Depends(require_api_key)])
async def chat_stream(req: ChatRequest) -> StreamingResponse:
    settings = get_settings()
    if settings.enable_guardrails:
        guard = guard_input(req.message)
        if not guard.allowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"blocked by guardrails: {guard.reason}",
            )
        message = guard.redacted or req.message
    else:
        message = req.message

    async def event_source():
        async for chunk in agent.stream(message):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_source(), media_type="text/event-stream")


@app.get(
    "/chat/history/{session_id}",
    response_model=HistoryResponse,
    dependencies=[Depends(require_api_key)],
)
async def chat_history(session_id: str) -> HistoryResponse:
    messages = [Message(**m) for m in store.get(session_id)]
    return HistoryResponse(session_id=session_id, messages=messages)
