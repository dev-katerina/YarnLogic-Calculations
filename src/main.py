import asyncio
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import neo4j, postgres
from api import patterns, assist

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


app = FastAPI(
    title="YarnLogic Calculations API",
    description="API for managing knitting patterns, stitches, relations, and tools.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(assist.router, prefix="/assist", tags=["assist"])
app.include_router(patterns.router, prefix="/pattern", tags=["patterns"])
