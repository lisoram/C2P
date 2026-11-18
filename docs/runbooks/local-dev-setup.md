# C2P – Local Development Setup

## Prerequisites

| Tool | Version | Install |
|---|---|---|
| Docker Desktop | Latest | https://www.docker.com/products/docker-desktop/ |
| Python | 3.12 | https://www.python.org/downloads/ |
| uv | Latest | `pip install uv` or https://docs.astral.sh/uv/getting-started/installation/ |
| Node.js | 24 LTS | https://nodejs.org/ |
| npm | Bundled with Node | — |

---

## 1. Clone and configure environment

```bash
git clone <repo-url>
cd C2P

# Backend env
cp backend/.env.example backend/.env
# Edit backend/.env and fill in your GEMINI_API_KEY.
# The other values match docker-compose defaults and don't need changing.

# Frontend env
cp frontend/.env.local.example frontend/.env.local
# NEXT_PUBLIC_API_URL is already set to http://localhost:8000
```

---

## 2. Start the infrastructure

```bash
docker compose up -d
```

This starts Postgres 16, MongoDB 7, and Qdrant. Wait until all three are healthy:

```bash
docker compose ps
```

All three should show `healthy`.

---

## 3. Run the backend

```bash
cd backend

# Create virtual environment and install dependencies
uv sync

# Apply Alembic migration (creates the drawings table)
uv run alembic upgrade head

# Start the server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API is now at http://localhost:8000.

---

## 4. Verify the health endpoint

```bash
curl http://localhost:8000/api/v1/health
```

Expected response (all services up):

```json
{
  "status": "ok",
  "services": {
    "postgres": "ok",
    "mongodb": "ok",
    "qdrant": "ok",
    "gemini": "ok"
  }
}
```

If a service is down, its value will be `"error"` and `status` will be `"degraded"`.

---

## 5. Run the tests

```bash
cd backend
uv run pytest -v
```

All unit and integration tests use mocked external clients — no infrastructure needed.

---

## 6. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000. You should see live per-service status.

---

## 7. Confirm the drawings table exists (optional)

```bash
docker compose exec postgres psql -U c2p -d c2p_db -c "\dt drawings"
```

Expected output: a row for the `drawings` table.

---

## Stopping everything

```bash
docker compose down
```

Add `-v` to also delete the data volumes: `docker compose down -v`
