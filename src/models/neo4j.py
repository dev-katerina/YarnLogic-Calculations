from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4
from neo4j.graph import Node

class Stitch(BaseModel):
    id: UUID
    type: str
    tool: str
    graph_id: UUID

    def to_neo4j(self):
        return {
            "id": str(self.id),
            "type": self.type,
            "tool": self.tool,
            "graph_id": str(self.graph_id),
        }
    
    @classmethod
    def from_neo4j(cls, node: Node) -> "Stitch":
        return cls(
            id=UUID(node["id"]),
            type=node["type"],
            tool=node["tool"],
            graph_id=UUID(node["graph_id"]),
        )


class Relation(BaseModel):
    id: UUID = uuid4()
    type: str
    graph_id: UUID

    def to_neo4j(self):
        return {
            "id": str(self.id),
            "type": self.type,
            "graph_id": str(self.graph_id),
        }
    
    @classmethod
    def from_neo4j(cls, node: Node) -> "Relation":
        return cls(
            id=UUID(node["id"]),
            type=node["type"],
            graph_id=UUID(node["graph_id"]),
        )


