from db.neo4j import get_data
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting application...")
    num = await get_data()
    logger.info(f"Data from Neo4j: {num}")
    logger.info("Application finished.")

if __name__ == "__main__":
    asyncio.run(main())