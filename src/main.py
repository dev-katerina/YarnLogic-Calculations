import asyncio
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import neo4j, postgres

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up the application...")
    neo4j.init_driver()
    postgres.init_db()

    yield

    logger.info("Shutting down the application...")
    await asyncio.gather(neo4j.close_driver(), postgres.close_db())


app = FastAPI(lifespan=lifespan)
