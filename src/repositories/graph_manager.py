from uuid import UUID

import neo4j
import logging
from typing import Dict, List, Any
from models.neo4j import Stitch, Relation

logger = logging.getLogger(__name__)


class GraphManager:
    def __init__(self, driver: neo4j.AsyncDriver) -> None:
        self.driver = driver

    async def add_node(self, node_data: Stitch) -> Dict[str, Any]:
        if not isinstance(node_data, Stitch):
            raise ValueError("node_data должен быть экземпляром класса Stitch")
        async with self.driver.session() as session:
            result = await session.run("CREATE (n:Node $props)", props=node_data)
            record = await result.single()
            return record
        
    async def get_node(self, node_id: UUID) -> Dict[str, Any]:
        async with self.driver.session() as session:
            result = await session.run(
                "MATCH (n:Node {id: $node_id}) RETURN n", node_id=node_id
            )
            record = await result.single()
            return record
        pass

    async def add_relationship(
        self, from_id: UUID, to_id: UUID, properties: Relation
    ) -> Dict[str, Any]:
        if not isinstance(properties, Relation):
            raise ValueError(
                "properties должен быть экземпляром класса Relation или None"
            )
        async with self.driver.session() as session:
            result = await session.run(
                """
                MATCH (a:Node {id: $from_id})
                MATCH (b:Node {id: $to_id})
                CREATE (a)-[:RELATIONSHIP]->(b)
                """,
                from_id=from_id,
                to_id=to_id,
                props=properties or {},
            )
            record = await result.single()
            return record
        pass

    async def query_graph(self, graph_id: UUID) -> List[Any]:
        async with self.driver.session() as session:
            result = await session.run(
                "MATCH (n:Node {graph_id: $graph_id}) RETURN n", graph_id=graph_id
            )
            records = await result.values()
            return records
        pass

    async def delete_node(self, node_id: UUID) -> bool:
        async with self.driver.session() as session:
            await session.run(
                "MATCH (n:Node {id: $node_id}) DETACH DELETE n", node_id=node_id
            )
            return True
        pass

    async def delete_relationship(self, relationship_id: UUID) -> bool:
        async with self.driver.session() as session:
            await session.run(
                "MATCH ()-[r]->() WHERE id(r) = $relationship_id DELETE r",
                relationship_id=relationship_id,
            )
            return True
        pass

    async def delete_graph(self, graph_id: UUID) -> bool:
        async with self.driver.session() as session:
            await session.run(
                "MATCH (n:Node {graph_id: $graph_id}) DETACH DELETE n", graph_id=graph_id
            )
            return True
        pass