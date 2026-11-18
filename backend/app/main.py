"""
FastAPI application entry point.

Responsibilities:
- Configure structured JSON logging (first, so every later import can log)
- Register routers
- Add request-logging middleware (logs method, path, status, duration, request_id)
- Fail loudly on startup if Postgres or MongoDB are unreachable
  (Qdrant and Gemini are checked on each /health call, not at startup,
   to keep startup fast and to let /health surface which one is actually down)
- Return RFC 7807-style error envelopes for 422 validation errors
"""

import time
import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logging import configure_logging, get_logger

# ── Logging must be configured before any other import that calls get_logger ──
configure_logging()
logger = get_logger(__name__)

from app.api.v1.router import router as v1_router  # noqa: E402  (import after logging)

app = FastAPI(
    title="C2P API",
    version="0.1.0",
    description="Computer-Aided Process Planning – Module 0 scaffold",
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(v1_router)


# ── Request logging middleware ────────────────────────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start = time.perf_counter()

    response = await call_next(request)

    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    logger.info(
        "request",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration_ms": duration_ms,
        },
    )
    response.headers["X-Request-Id"] = request_id
    return response


# ── Standard error envelope for validation errors (422) ──────────────────────
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request payload validation failed",
                "details": {"errors": exc.errors()},
            }
        },
    )
