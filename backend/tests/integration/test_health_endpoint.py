"""
Integration tests for GET /api/v1/health.
Uses Starlette's synchronous TestClient (wraps the ASGI app in its own
event loop via anyio) so these tests run reliably without an external
event-loop fixture.
All external clients are mocked.
"""

from unittest.mock import AsyncMock, patch

from starlette.testclient import TestClient


def _make_client():
    """Import the app here so conftest env vars are already set."""
    from app.main import app
    return TestClient(app, raise_server_exceptions=True)


def test_health_endpoint_returns_200_all_ok():
    """The /api/v1/health endpoint returns 200 with all services ok."""
    with (
        patch("app.api.v1.health.check_postgres", new_callable=AsyncMock),
        patch("app.api.v1.health.check_mongodb", new_callable=AsyncMock),
        patch("app.api.v1.health.check_qdrant", new_callable=AsyncMock),
        patch("app.api.v1.health.check_gemini", new_callable=AsyncMock),
    ):
        client = _make_client()
        response = client.get("/api/v1/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["services"]["postgres"] == "ok"
    assert body["services"]["mongodb"] == "ok"
    assert body["services"]["qdrant"] == "ok"
    assert body["services"]["gemini"] == "ok"


def test_health_endpoint_degraded_when_postgres_down():
    """The /api/v1/health endpoint reports degraded when postgres fails."""
    async def _fail():
        raise ConnectionRefusedError("postgres unreachable")

    with (
        patch("app.api.v1.health.check_postgres", side_effect=_fail),
        patch("app.api.v1.health.check_mongodb", new_callable=AsyncMock),
        patch("app.api.v1.health.check_qdrant", new_callable=AsyncMock),
        patch("app.api.v1.health.check_gemini", new_callable=AsyncMock),
    ):
        client = _make_client()
        response = client.get("/api/v1/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "degraded"
    assert body["services"]["postgres"] == "error"
    assert body["services"]["mongodb"] == "ok"


def test_health_endpoint_has_request_id_header():
    """Every response includes an X-Request-Id header."""
    with (
        patch("app.api.v1.health.check_postgres", new_callable=AsyncMock),
        patch("app.api.v1.health.check_mongodb", new_callable=AsyncMock),
        patch("app.api.v1.health.check_qdrant", new_callable=AsyncMock),
        patch("app.api.v1.health.check_gemini", new_callable=AsyncMock),
    ):
        client = _make_client()
        response = client.get("/api/v1/health")

    assert "x-request-id" in response.headers
    assert len(response.headers["x-request-id"]) == 36  # UUID format
