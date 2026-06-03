from abc import ABC, abstractmethod
import logging

from models.neo4j import Stitch, Relation
import neo4j
from typing import List, Optional, Tuple
from uuid import UUID

logger = logging.getLogger(__name__)

class GraphManager(ABC):
    @abstractmethod
    async def add_node(self, stitch: Stitch):
        pass

    @abstractmethod
    async def get_node(self, node_id: UUID) -> Stitch:
        pass

    @abstractmethod
    async def change_node(self, stitch: Stitch):
        pass

    @abstractmethod
    async def add_relationship(self, from_id: UUID, to_id: UUID, relation: Relation):
        pass

    @abstractmethod
    async def get_relationship(self, relationship_id: UUID) -> Relation:
        pass
    
    @abstractmethod
    async def change_relationship(self, relationship_id: UUID, from_id: UUID, to_id: UUID, relation: Relation):
        pass

    @abstractmethod
    async def query_graph(self, graph_id: UUID) -> List[Tuple[Stitch, Optional[Relation], Optional[Stitch]]]:
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

    @abstractmethod
    async def commit(self):
        pass


class GraphManagerNeo4j(GraphManager):
    def __init__(self, session: neo4j.AsyncSession):
        self.session = session

    async def add_node(self, stitch: Stitch):
        node_data = stitch.to_neo4j()

        result = await self.session.run("CREATE (n:Node $props)", props=node_data)
        record = await result.single()

    async def get_node(self, node_id: UUID) -> Stitch:
        result = await self.session.run(
            "MATCH (n:Node {id: $node_id}) RETURN n", node_id=str(node_id)
        )
        record = await result.single()
        if record is None:
            return None
        return Stitch.from_neo4j(record["n"])

    async def change_node(self, stitch: Stitch):
        node_data = stitch.to_neo4j()
        
        result = await self.session.run(
            "MATCH (n:Node {id: $node_id}) SET n += $props RETURN n",
            node_id=str(stitch.id),
            props=node_data,
        )
        record = await result.single()

    async def add_relationship(self, from_id: UUID, to_id: UUID, relation: Relation):
        relation_data = relation.to_neo4j()

        result = await self.session.run(
            """
            MATCH (a:Node {id: $from_id}), (b:Node {id: $to_id})
            CREATE (a)-[r:RELATION $props]->(b)
            RETURN r
            """,
            from_id=str(from_id),
            to_id=str(to_id),
            props=relation_data,
        )

        record = await result.single()
        

    async def get_relationship(self, relationship_id: UUID) -> Relation:
        result = await self.session.run(
            "MATCH ()-[r:RELATION {id: $relationship_id}]-() RETURN r", relationship_id=str(relationship_id)
        )
        record = await result.single()
        if record is None:
            return None
        return Relation.from_neo4j(record["r"])

    async def change_relationship(self, from_id: UUID, to_id: UUID, relation: Relation):
        relation_data = relation.to_neo4j()
        result = await self.session.run(
            """
            MATCH ()-[r:RELATION {id: $relation_id}]->()
            DELETE r

            WITH $from_id AS from_id, $to_id AS to_id, $new_props AS new_props

            MATCH (new_from:Node {id: from_id})
            MATCH (new_to:Node {id: to_id})

            CREATE (new_from)-[new_r:RELATION {id: $relation_id}]->(new_to)
            SET new_r = new_props

            RETURN new_r
            """,
            relation_id=str(relation.id),
            from_id=str(from_id),
            to_id=str(to_id),
            new_props=relation_data,
        )
        record = await result.single()

        if record is None:
            raise RuntimeError("Relationship not found or not updated")




    async def query_graph(self, graph_id: UUID) -> List[Tuple[Stitch, Optional[Relation], Optional[Stitch]]]:
        """
        Возвращает список узлов и рёбер графа в виде:
        [(Stitch(..), Relation(..) | None, Stitch(..) | None), ...]
        """
        result = await self.session.run(
            """
            MATCH (n:Node {graph_id: $graph_id})
            OPTIONAL MATCH (n)-[r:RELATION]->(m:Node)
            RETURN n, r, m
            """,
            graph_id=str(graph_id)
        )
        
        edges = []
        async for record in result:
            n_node = record["n"]   # Node
            r_rel = record.get("r")    # Relationship or None
            m_node = record.get("m")   # Node or None
            
            from_stitch = Stitch.from_neo4j(n_node)
            relation = Relation.from_neo4j(r_rel) if r_rel is not None else None
            to_stitch = Stitch.from_neo4j(m_node) if m_node is not None else None
            
            edges.append((from_stitch, relation, to_stitch))
        return edges

    async def delete_node(self, node_id: UUID):
        
        await self.session.run("MATCH (n:Node {id: $node_id}) DELETE n", node_id=str(node_id))

    async def delete_relationship(self, relationship_id: UUID):
        
        await self.session.run("MATCH ()-[r:RELATION {id: $relationship_id}]-() DELETE r", relationship_id=str(relationship_id))

    async def delete_graph(self, graph_id: UUID):
        
            await self.session.run("MATCH (n:Node)-[r:RELATION]->(m:Node) DELETE n, r, m")

    async def commit(self):
        # Neo4j драйвер автоматически коммитит транзакции после каждого запроса, 
        # поэтому здесь нет необходимости в явном коммите.
        pass