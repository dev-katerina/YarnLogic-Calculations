import asyncio
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assist.router, prefix="/assist", tags=["assist"])
app.include_router(patterns.router, prefix="/pattern", tags=["patterns"])
