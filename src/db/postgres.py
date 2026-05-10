from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from core.config import settings
import logging

logger = logging.getLogger(__name__)


DATABASE_URL = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"

engine: AsyncEngine | None = None
SessionLocal: async_sessionmaker[AsyncSession] | None = None

def init_db() -> None:
    global engine, SessionLocal

    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )

    SessionLocal = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    logger.info("PostgreSQL database initialized")

async def close_db() -> None:
    if engine:
        await engine.dispose()
        logger.info("PostgreSQL database connection closed")