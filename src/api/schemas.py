from pydantic import BaseModel, Field
from typing import List, Optional

from uuid import UUID

"""Инструменты"""


class Tool(BaseModel):
    name: str
    description: Optional[str] = None


"""Петли"""


class StitchType(BaseModel):
    name: str
    description: Optional[str] = None


class CreateStitch(BaseModel):
    type: str
    tool: str


class ReadStitch(CreateStitch):
    id: UUID
    graph_id: UUID


"""Cвязи"""


class RelationType(BaseModel):
    name: str
    description: Optional[str] = None


class CreateRelation(BaseModel):
    type: str
    graph_id: UUID
    base_stitch_id: UUID
    target_stitch_id: UUID


class ReadRelation(CreateRelation):
    id: UUID


"""Схемы"""


class CreatePattern(BaseModel):
    name: str


class ReadPattern(CreatePattern):
    graph_id: UUID


class ReadPatternDetail(BaseModel):
    pattern: ReadPattern
    stitches: List[ReadStitch]
    relations: List[ReadRelation]
