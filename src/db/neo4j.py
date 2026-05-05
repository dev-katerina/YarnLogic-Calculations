import logging
from neo4j import AsyncGraphDatabase
from .core.config import settings

logger = logging.getLogger(__name__)

driver = AsyncGraphDatabase.driver(
    f"bolt://{settings.graphdb_host}:{settings.graphdb_port}",
    auth=(settings.graphdb_user, settings.graphdb_password)
)

async def get_data():
    logger.info("Connecting to Neo4j database...")
    async with driver.session() as session:
        logger.info("Executing query: RETURN 1 AS num")
        result = await session.run("RETURN 1 AS num")
        record = await result.single()
        num = record["num"]
        logger.info(f"Retrieved data: {num}")
        return num