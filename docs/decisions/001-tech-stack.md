# ADR 001 – Tech Stack for Module 0

**Date:** 2026-11-17
**Status:** Accepted

## Decision

| Concern | Choice | Reason |
|---|---|---|
| Local services | docker-compose | Reproducible; one command for all devs |
| Python package manager | uv + Python 3.12 | Fast installs, clean lockfile |
| Node version | Node 24 LTS (Krypton) | Current Active LTS as of Oct 2025 |
| Node package manager | npm | Standard; already available everywhere |
| Qdrant collection | `drawings`, vector size 768 | Placeholder pending embedding model selection |
| Gemini model (health ping) | `gemini-3.5-flash-lite` | Cheapest currently-stable Flash-class model (\$0.30/1M in tokens); `gemini-2.0-flash-lite` is shut down |
| Branch naming | `chore/module-0-scaffold` | `chore` prefix signals infrastructure work |
