import pytest
import asyncio
import pytest_asyncio
from db.postgres import init_db, close_db, get_sessionmaker
from db.neo4j import init_driver, close_driver, get_driver
from repositories.graph_manager import GraphManagerNeo4j

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

        await session.begin_nested()

        try:
            yield session
        finally:
            await session.rollback()
            await session.close()

@pytest_asyncio.fixture(scope="function")
async def neo4j_driver():
    init_driver()
    yield
    await close_driver()

import pytest

@pytest_asyncio.fixture(scope="function")
async def neo4j_session(neo4j_driver):
    driver = get_driver()

    async with driver.session() as session:
        yield session

        # cleanup после теста
        await session.run("MATCH (n) DETACH DELETE n")