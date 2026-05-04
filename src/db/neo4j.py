import logging
from neo4j import AsyncGraphDatabase

logger = logging.getLogger(__name__)

driver = AsyncGraphDatabase.driver(
    "bolt://graphdb:7687",
    auth=("neo4j", "testpassword")
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