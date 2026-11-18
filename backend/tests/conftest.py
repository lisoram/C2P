"""
Root conftest.py for the backend test suite.

Sets required environment variables BEFORE any app module is imported.
This is necessary because pydantic-settings instantiates Settings() at
module load time (as a module-level singleton in app.core.config).

These are dummy values — no real services are contacted in unit/integration
tests (all external clients are mocked).
"""

import os

# Set env vars before any app import happens (pytest_configure runs first)
def pytest_configure(config):
    test_env = {
        "POSTGRES_HOST": "localhost",
        "POSTGRES_PORT": "5432",
        "POSTGRES_DB": "c2p_test",
        "POSTGRES_USER": "c2p",
        "POSTGRES_PASSWORD": "c2p_secret",
        "MONGODB_URI": "mongodb://c2p:c2p_secret@localhost:27017",
        "MONGODB_DB": "c2p_test",
        "QDRANT_HOST": "localhost",
        "QDRANT_PORT": "6333",
        "QDRANT_COLLECTION": "drawings",
        "QDRANT_VECTOR_SIZE": "768",
        "GEMINI_API_KEY": "test-key-not-real",
        "GEMINI_MODEL": "gemini-3.5-flash-lite",
        "APP_ENV": "test",
        "LOG_LEVEL": "WARNING",
    }
    for key, value in test_env.items():
        os.environ.setdefault(key, value)
