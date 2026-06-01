from typing import List
from uuid import uuid4

from core.errors import NotFoundError, AlreadyExistsError

from repositories import pattern, relation_type, stitch_type, tool_type
from models.postgres import Pattern, RelationType, StitchType, Tool
from models.neo4j import Stitch , Relation
from api.schemas import (
    StitchType as ApiStitchType,
    CreatePattern,
    ReadPattern,
    CreateStitch,
    ReadPatternDetail,
    ReadStitch,
    CreateRelation,
    ReadRelation,
)


class AssistService:
    def __init__(
        self,
        pattern_repo: pattern.PatternRepository,
        stitch_type_repo: stitch_type.StitchTypeRepository,
        relation_type_repo: relation_type.RelationTypeRepository,
        tool_type_repo: tool_type.ToolRepository,
    ):
        self.pattern_repo = pattern_repo
        self.stitch_type_repo = stitch_type_repo
        self.relation_type_repo = relation_type_repo
        self.tool_type_repo = tool_type_repo

    async def get_stitch_types(self) -> List[ApiStitchType]:
        stitch_types = await self.stitch_type_repo.get_all()
        if len(stitch_types) == 0:
            raise NotFoundError
        return [ApiStitchType(name=st.name, description=st.description) for st in stitch_types]

    async def get_stitch_type(self, name: str) -> ApiStitchType:
        result = await self.stitch_type_repo.get_by_name(name)
        if result is None:
            raise NotFoundError
        return ApiStitchType(name=result.name, description=result.description)

    async def create_stitch_type(self, stitch_type: ApiStitchType) -> ApiStitchType:
        existing = await self.stitch_type_repo.get_by_name(stitch_type.name)
        if existing:
            raise AlreadyExistsError
        
        new_stitch_type = StitchType(name=stitch_type.name, description=stitch_type.description)
        created = await self.stitch_type_repo.create(new_stitch_type)
        await self.stitch_type_repo.commit()
        return ApiStitchType(name=created.name, description=created.description)
    
    async def delete_stitch_type(self, name: str) -> None:
        result = await self.stitch_type_repo.get_by_name(name)
        if result is None:
            raise NotFoundError
        await self.stitch_type_repo.delete(result)
        await self.stitch_type_repo.commit()