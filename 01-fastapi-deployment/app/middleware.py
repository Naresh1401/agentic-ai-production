"""Request middleware: correlation ID, structured logging, latency metric."""
from __future__ import annotations

import json
import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from .metrics import metrics

logger = logging.getLogger("agentic")


class ObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("x-request-id") or uuid.uuid4().hex[:12]
        start = time.perf_counter()
        is_error = False
        try:
            response = await call_next(request)
            is_error = response.status_code >= 500
            return response
        except Exception:
            is_error = True
            raise
        finally:
            latency_ms = (time.perf_counter() - start) * 1000
            metrics.observe_request(latency_ms, is_error=is_error)
            logger.info(
                json.dumps(
                    {
                        "request_id": request_id,
                        "method": request.method,
                        "path": request.url.path,
                        "latency_ms": round(latency_ms, 2),
                        "error": is_error,
                    }
                )
            )
