"""Module 1 concern: the FastAPI service that exposes the capstone agent."""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from . import agent
from .config import get_settings
from .observability import memory, metrics
from .tracing import setup_tracing


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    session_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    source: str
    model: str | None = None
    cached: bool = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_tracing()
    yield


app = FastAPI(title="Support Agent (Capstone)", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins_list,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics")
async def get_metrics() -> dict:
    return metrics.snapshot()


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    try:
        result = await agent.answer(req.message, req.session_id)
    except agent.GuardrailBlocked as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"blocked by guardrails: {exc.reason}",
        ) from exc
    return ChatResponse(**result)


@app.post("/chat/stream")
async def chat_stream(req: ChatRequest) -> StreamingResponse:
    try:
        result = await agent.answer(req.message, req.session_id)
    except agent.GuardrailBlocked as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"blocked by guardrails: {exc.reason}",
        ) from exc

    async def event_source():
        for word in result["answer"].split():
            yield f"data: {word} \n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_source(), media_type="text/event-stream")


@app.get("/chat/history/{session_id}")
async def history(session_id: str) -> dict:
    return {"session_id": session_id, "messages": memory.get(session_id)}
