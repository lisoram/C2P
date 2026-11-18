# C2P – Computer-Aided Process Planning

An AI-powered platform for engineering drawing intelligence.

## Quick start

See [docs/runbooks/local-dev-setup.md](docs/runbooks/local-dev-setup.md) for the full setup and run guide.

**TL;DR:**

```bash
# 1. Fill in .env files
cp backend/.env.example backend/.env       # add your GEMINI_API_KEY
cp frontend/.env.local.example frontend/.env.local

# 2. Start infrastructure
docker compose up -d

# 3. Backend
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --port 8000

# 4. Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Then open http://localhost:3000.

## Project structure

```
C2P/
├── backend/          # FastAPI + Python 3.12
├── frontend/         # Next.js 15, App Router
├── docs/             # Architecture, module notes, decisions, runbooks
└── docker-compose.yml
```

## Documentation

- [Local dev setup](docs/runbooks/local-dev-setup.md)
- [Architecture overview](docs/architecture/00-overview.md)
- [Module 0 notes](docs/modules/00-module-0-skeleton.md)
- [Tech stack decision](docs/decisions/001-tech-stack.md)
- [AI Assistant context](docs/C2P_AI_Assistant_Context.md)
