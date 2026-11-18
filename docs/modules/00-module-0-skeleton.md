# Module 0 – Skeleton Scaffold

**Status:** Complete
**Branch:** `chore/module-0-scaffold`

## What was built

A running, connected scaffold that proves every service in the stack can talk to every other service, with zero business logic.

### Backend (FastAPI + Python 3.12)
- `GET /api/v1/health` — checks Postgres, MongoDB, Qdrant, Gemini in parallel
- Pydantic models for all responses; 422 returns a structured error envelope
- Structured JSON logging on every request (method, path, status, duration, request_id)
- `pydantic-settings` reads all config from `.env`
- Postgres session factory (SQLAlchemy async + asyncpg)
- MongoDB GridFS round-trip test (Motor)
- Qdrant collection creation if not exists
- Gemini API trivial generate call (model: `gemini-3.5-flash-lite`)
- Alembic initialized with one migration: `drawings (id UUID PK, created_at TIMESTAMPTZ)`

### Frontend (Next.js 15, App Router)
- Single page calls `/api/v1/health` live on every render
- Shows per-service status badges (green/red)
- Handles backend-unreachable gracefully (yellow warning, no crash)

### Infrastructure
- `docker-compose.yml` — Postgres 16, MongoDB 7, Qdrant 1.13.6

## What was NOT built
- No business logic of any kind
- No file upload
- No authentication
- Module 1 onwards
