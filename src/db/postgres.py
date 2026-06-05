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


def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    if SessionLocal is None:
        raise RuntimeError("SessionLocal is not initialized")

    return SessionLocal


async def close_db() -> None:
    if engine:
        await engine.dispose()
        logger.info("PostgreSQL database connection closed")


async def get_session() -> AsyncSession:
    if SessionLocal is None:
        raise RuntimeError("SessionLocal is not initialized")

    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise