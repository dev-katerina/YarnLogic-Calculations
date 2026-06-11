from pydantic import BaseModel, Field
from typing import List

from uuid import UUID

"""Инструменты"""


class Tool(BaseModel):
    name: str = Field(..., title="Tool name", description="Unique name of the tool.")
    description: str | None = Field(
        None,
        title="Tool description",
        description="Optional human-readable description of the tool.",
    )


"""Петли"""


class StitchType(BaseModel):
    name: str = Field(
        ...,
        title="Stitch type name",
        description="Unique identifier for the stitch type.",
    )
    description: str | None = Field(
        None,
        title="Stitch type description",
        description="Optional human-readable description of this stitch type.",
    )


class CreateStitch(BaseModel):
    type: str = Field(
        ..., title="Stitch type", description="The stitch type used for this stitch."
    )
    tool: str = Field(
        ...,
        title="Tool name",
        description="The name of the tool required for the stitch.",
    )


class ReadStitch(CreateStitch):
    id: UUID = Field(
        ..., title="Stitch ID", description="Unique identifier of the stitch."
    )
    graph_id: UUID = Field(
        ...,
        title="Pattern ID",
        description="Identifier of the pattern this stitch belongs to.",
    )


"""Cвязи"""


class RelationType(BaseModel):
    name: str = Field(
        ...,
        title="Relation type name",
        description="Unique identifier for the relation type.",
    )
    description: str | None = Field(
        None,
        title="Relation type description",
        description="Optional human-readable description of this relation type.",
    )


class CreateRelation(BaseModel):
    type: str = Field(
        ...,
        title="Relation type",
        description="Type of relation that connects two stitches.",
    )
    graph_id: UUID = Field(
        ...,
        title="Pattern ID",
        description="Identifier of the pattern where the relation is created.",
    )
    base_stitch_id: UUID = Field(
        ...,
        title="Base stitch ID",
        description="Identifier of the base stitch in the relation.",
    )
    target_stitch_id: UUID = Field(
        ...,
        title="Target stitch ID",
        description="Identifier of the target stitch in the relation.",
    )


class ReadRelation(CreateRelation):
    id: UUID = Field(
        ..., title="Relation ID", description="Unique identifier of the relation."
    )


"""Схемы"""


class CreatePattern(BaseModel):
    name: str = Field(
        ..., title="Pattern name", description="The name of the pattern graph."
    )


class ReadPattern(CreatePattern):
    graph_id: UUID = Field(
        ..., title="Pattern ID", description="Unique identifier of the pattern graph."
    )


class ReadPatternDetail(BaseModel):
    pattern: ReadPattern = Field(
        ..., title="Pattern", description="The pattern metadata."
    )
    stitches: List[ReadStitch] = Field(
        ..., title="Stitches", description="List of stitches in the pattern."
    )
    relations: List[ReadRelation] = Field(
        ..., title="Relations", description="List of relations between stitches."
    )

    class Config:
        schema_extra = {
            "example": {
                "pattern": {
                    "graph_id": "11111111-1111-1111-1111-111111111111",
                    "name": "Sample pattern",
                },
                "stitches": [
                    {
                        "id": "22222222-2222-2222-2222-222222222222",
                        "graph_id": "11111111-1111-1111-1111-111111111111",
                        "type": "single",
                        "tool": "hook",
                    }
                ],
                "relations": [
                    {
                        "id": "33333333-3333-3333-3333-333333333333",
                        "type": "join",
                        "graph_id": "11111111-1111-1111-1111-111111111111",
                        "base_stitch_id": "22222222-2222-2222-2222-222222222222",
                        "target_stitch_id": "22222222-2222-2222-2222-222222222222",
                    }
                ],
            }
        }
