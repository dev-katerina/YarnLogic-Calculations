from abc import ABC, abstractmethod
import logging

from sqlalchemy import UUID
from models.neo4j import Stitch, Relation
from typing import List
import neo4j

logger = logging.getLogger(__name__)

class GraphManager(ABC):
    @abstractmethod
    async def add_node(self, node_data: Stitch):
        pass

    @abstractmethod
    async def get_node(self, node_id: UUID) -> Stitch:
        pass

    @abstractmethod
    async def change_node(self, node_id: UUID, node_data: Stitch):
        pass

    @abstractmethod
    async def add_relationship(self, from_id: UUID, to_id: UUID, relation_data: Relation):
        pass

    @abstractmethod
    async def change_relationship(self, relationship_id: UUID, from_id: UUID, to_id: UUID, relation_data: Relation):
        pass

    @abstractmethod
    async def query_graph(self, graph_id: UUID) -> {List[Stitch], List[Relation]}:
        pass

    @abstractmethod
    async def delete_node(self, node_id: UUID):
        pass

    @abstractmethod
    async def delete_relationship(self, relationship_id: UUID):
        pass

    @abstractmethod
    async def delete_graph(self, graph_id: UUID):
        pass


class GraphManagerNeo4j(GraphManager):
    def __init__(self, driver: neo4j.AsyncDriver):
        self.driver = driver

    async def add_node(self, node_data: Stitch):
        with self.driver.session() as session:
            result = await session.run("CREATE (n:Node $props)", props=node_data)
            record = await result.single()
            return record

    async def get_node(self, node_id: UUID) -> Stitch:
        async with self.driver.session() as session:
            result = await session.run(
                "MATCH (n:Node {id: $node_id}) RETURN n", node_id=node_id
            )
            record = await result.single()
            return record
        pass

    async def change_node(self, node_id: UUID, node_data: Stitch):
        async with self.driver.session() as session:
            result = await session.run(
                "MATCH (n:Node {id: $node_id}) SET n += $props RETURN n",
                node_id=node_id,
                props=node_data,
            )
            record = await result.single()
            return record

    async def add_relationship(self, from_id: UUID, to_id: UUID, relation_data: Relation):
        async with self.driver.session() as session:
            result = await session.run(
                "MATCH (a:Node {id: $from_id}), (b:Node {id: $to_id}) CREATE (a)-[r:RELATION {id: $relation_id}]->(b) RETURN r",
                from_id=from_id,
                to_id=to_id,
                relation_id=relation_data.id,
            )
            record = await result.single()
            return record

    async def change_relationship(self, relationship_id: UUID, from_id: UUID, to_id: UUID, relation_data: Relation):
        async with self.driver.session() as session:
            result = await session.run(
                "MATCH (a:Node {id: $from_id}), (b:Node {id: $to_id}), (r:RELATION {id: $relationship_id}) SET r += $props RETURN r",
                from_id=from_id,
                to_id=to_id,
                relationship_id=relationship_id,
                props=relation_data,
            )
            record = await result.single()
            return record

    async def query_graph(self, graph_id: UUID) -> {List[Stitch], List[Relation]}:
        async with self.driver.session() as session:
            result = await session.run(
                "MATCH (n:Node)-[r:RELATION]->(m:Node) RETURN n, r, m"
            )
            nodes = []
            relationships = []
            async for record in result:
                nodes.append(record["n"])
                relationships.append(record["r"])
            return {"nodes": nodes, "relationships": relationships}

    async def delete_node(self, node_id: UUID):
        async with self.driver.session() as session:
            await session.run("MATCH (n:Node {id: $node_id}) DELETE n", node_id=node_id)

    async def delete_relationship(self, relationship_id: UUID):
        async with self.driver.session() as session:
            await session.run("MATCH ()-[r:RELATION {id: $relationship_id}]-() DELETE r", relationship_id=relationship_id)

    async def delete_graph(self, graph_id: UUID):
        async with self.driver.session() as session:
            await session.run("MATCH (n:Node)-[r:RELATION]->(m:Node) DELETE n, r, m")