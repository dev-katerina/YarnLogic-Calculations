from elasticsearch import AsyncElasticsearch
from core.config import settings
import logging

logger = logging.getLogger(__name__)

es_client: AsyncElasticsearch | None = None


def init_db() -> AsyncElasticsearch:
    global es_client

    if es_client is None:
        es_client = AsyncElasticsearch(
            hosts=settings.es_hosts
        )
        logger.info("ElasticSearch database initialized")
    else:
        logger.info("ElasticSearch database already initialized")

    return es_client


async def close_db() -> None:
    global es_client

    if es_client is None:
        logger.info("ElasticSearch database connection already closed")
        return

    await es_client.close()
    logger.info("ElasticSearch database connection closed")
    es_client = None

    