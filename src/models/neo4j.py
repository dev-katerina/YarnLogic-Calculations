from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class Stitch(BaseModel):
    id: UUID
    type: str
    tool: str
    graph_id: UUID

class Relation(BaseModel):
    id: UUID
    type: str
    graph_id: UUID