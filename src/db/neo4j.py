import logging
from neo4j import AsyncGraphDatabase
from core.config import settings

logger = logging.getLogger(__name__)

driver = None


def init_driver() -> None:
    global driver

    driver = AsyncGraphDatabase.driver(
        f"bolt://{settings.graphdb_host}:{settings.graphdb_port}",
        auth=(settings.graphdb_user, settings.graphdb_password),
    )
    logger.info("Neo4j driver initialized")


async def close_driver() -> None:
    global driver

    if driver:
        await driver.close()
        logger.info("Neo4j driver closed")

def get_driver() -> AsyncGraphDatabase:
    global driver

    if not driver:
        raise Exception("Neo4j driver not initialized. Call init_driver() first.")
    
    return driver