import pytest_asyncio
from db.postgres import init_db, close_db, get_sessionmaker


@pytest_asyncio.fixture(scope="session")
async def init_test_db():
    init_db()
    yield
    await close_db()

@pytest_asyncio.fixture
async def db_session(init_test_db):
    SessionLocal = get_sessionmaker()

    async with SessionLocal() as session:
        yield session