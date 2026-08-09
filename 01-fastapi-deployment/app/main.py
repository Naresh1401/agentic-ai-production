"""FastAPI entrypoint for the agent service."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from . import agent
from .config import get_settings
from .schemas import ChatRequest, ChatResponse

app = FastAPI(title="Agentic AI Service", version="0.1.0")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    reply, mock = await agent.run(req.message)
    return ChatResponse(reply=reply, model=get_settings().default_model, mock=mock)


@app.post("/chat/stream")
async def chat_stream(req: ChatRequest) -> StreamingResponse:
    async def event_source():
        async for chunk in agent.stream(req.message):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_source(), media_type="text/event-stream")
