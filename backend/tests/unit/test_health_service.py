"""
Unit tests for the health service layer.
Tests _probe() and health() logic directly — no HTTP layer involved.
Uses asyncio.run() so these work without any event-loop fixture.
"""

import asyncio
from unittest.mock import AsyncMock, patch


def test_probe_returns_ok_on_success():
    """_probe returns ('service', 'ok') when the coroutine succeeds."""
    from app.api.v1.health import _probe

    async def _run():
        async def good():
            pass
        return await _probe("postgres", good())

    name, status = asyncio.run(_run())
    assert name == "postgres"
    assert status == "ok"


def test_probe_returns_error_on_failure():
    """_probe returns ('service', 'error') when the coroutine raises."""
    from app.api.v1.health import _probe

    async def _run():
        async def bad():
            raise ConnectionRefusedError("unreachable")
        return await _probe("mongodb", bad())

    name, status = asyncio.run(_run())
    assert name == "mongodb"
    assert status == "error"


def test_health_all_ok():
    """health() returns status='ok' when all probes succeed."""
    from app.api.v1.health import health

    async def _run():
        with (
            patch("app.api.v1.health.check_postgres", new_callable=AsyncMock),
            patch("app.api.v1.health.check_mongodb", new_callable=AsyncMock),
            patch("app.api.v1.health.check_qdrant", new_callable=AsyncMock),
            patch("app.api.v1.health.check_gemini", new_callable=AsyncMock),
        ):
            return await health()

    response = asyncio.run(_run())
    assert response.status == "ok"
    assert response.services.postgres == "ok"
    assert response.services.mongodb == "ok"
    assert response.services.qdrant == "ok"
    assert response.services.gemini == "ok"


def test_health_one_service_down():
    """health() returns status='degraded' and names the failing service."""
    from app.api.v1.health import health

    async def fail():
        raise RuntimeError("down")

    async def _run():
        with (
            patch("app.api.v1.health.check_postgres", new_callable=AsyncMock),
            patch("app.api.v1.health.check_mongodb", side_effect=fail),
            patch("app.api.v1.health.check_qdrant", new_callable=AsyncMock),
            patch("app.api.v1.health.check_gemini", new_callable=AsyncMock),
        ):
            return await health()

    response = asyncio.run(_run())
    assert response.status == "degraded"
    assert response.services.mongodb == "error"
    assert response.services.postgres == "ok"
    assert response.services.qdrant == "ok"
    assert response.services.gemini == "ok"


def test_probe_logs_exception_type_when_message_is_empty(caplog):
    """TimeoutError has an empty str(); the log must still show type and a non-empty error."""
    import logging
    from app.api.v1.health import _probe

    async def _run():
        async def timeout():
            raise TimeoutError()
        return await _probe("postgres", timeout())

    with caplog.at_level(logging.ERROR, logger="app.api.v1.health"):
        name, status = asyncio.run(_run())

    assert (name, status) == ("postgres", "error")
    record = caplog.records[-1]
    assert record.error_type == "TimeoutError"
    assert record.error != ""
