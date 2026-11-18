"""
Postgres session factory (SQLAlchemy async) and ORM base.
Alembic uses the sync DSN; the app uses the async engine below.
"""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

engine = create_async_engine(
    settings.postgres_dsn_async,
    echo=False,
    pool_pre_ping=True,  # drops dead connections before handing them out
    connect_args={"timeout": 2.0},
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """All ORM models inherit from this base."""
    pass


async def check_postgres() -> None:
    """
    Run a trivial round-trip query.
    Raises an exception (loud failure) if Postgres is unreachable.
    """
    async with AsyncSessionLocal() as session:
        await session.execute(text("SELECT 1"))
    logger.info("Postgres connection verified")
