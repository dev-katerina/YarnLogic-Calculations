import pytest
import asyncio
import pytest_asyncio
from db.postgres import init_db, close_db, get_sessionmaker

@pytest_asyncio.fixture(scope="function") 
async def init_test_db(): 
    init_db() 
    yield 
    await close_db() 
    
@pytest_asyncio.fixture(scope="function")
async def db_session(init_test_db):
    SessionLocal = get_sessionmaker()

    async with SessionLocal() as session:
        await session.begin()

        # SAVEPOINT (очень важно)
        await session.begin_nested()

        try:
            yield session
        finally:
            await session.rollback()
            await session.close()