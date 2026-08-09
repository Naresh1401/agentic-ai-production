"""Request/response schemas for the chat API."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=8000)
    session_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    model: str
    mock: bool = False
