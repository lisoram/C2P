"""
GET /api/v1/health

Checks each downstream service independently.
- Returns HTTP 200 with status "ok" when all pass.
- Returns HTTP 200 with status "degraded" and the failing service named when any fail.
  (HTTP 200 so load-balancers don't remove the pod; the body carries the detail.)
"""

import asyncio
from typing import Any

from fastapi import APIRouter

from app.core.db import check_postgres
from app.core.gemini import check_gemini
from app.core.logging import get_logger
from app.core.mongo import check_mongodb
from app.core.qdrant import check_qdrant
from app.models.health import HealthResponse, ServiceStatuses

router = APIRouter()
logger = get_logger(__name__)


async def _probe(name: str, coro) -> tuple[str, str]:
    """Run a check coroutine and return (name, 'ok'|'error')."""
    try:
        await coro
        return name, "ok"
    except Exception as exc:
        # str(exc) is empty for some exceptions (e.g. TimeoutError), so always log the type
        # and fall back to repr() when the message is blank.
        logger.error(
            "Service health check failed",
            extra={
                "service": name,
                "error_type": type(exc).__name__,
                "error": str(exc) or repr(exc),
            },
        )
        return name, "error"


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns the connection status of every downstream service.",
    tags=["health"],
)
async def health() -> Any:
    results = await asyncio.gather(
        _probe("postgres", check_postgres()),
        _probe("mongodb", check_mongodb()),
        _probe("qdrant", check_qdrant()),
        _probe("gemini", check_gemini()),
    )

    statuses: dict[str, str] = dict(results)
    overall = "ok" if all(v == "ok" for v in statuses.values()) else "degraded"

    return HealthResponse(
        status=overall,
        services=ServiceStatuses(**statuses),
    )
