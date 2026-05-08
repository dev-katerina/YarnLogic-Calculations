import logging
from neo4j import AsyncGraphDatabase
from core.config import settings

logger = logging.getLogger(__name__)

driver = AsyncGraphDatabase.driver(
    f"bolt://{settings.graphdb_host}:{settings.graphdb_port}",
    auth=(settings.graphdb_user, settings.graphdb_password)
)