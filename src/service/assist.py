from typing import List
from uuid import uuid4

from core.errors import NotFoundError, AlreadyExistsError

from repositories import pattern, relation_type, stitch_type, tool_type
from models.postgres import Pattern, RelationType, StitchType, Tool
from models.neo4j import Stitch, Relation
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
        return [
            ApiStitchType(name=st.name, description=st.description)
            for st in stitch_types
        ]

    async def get_stitch_type(self, name: str) -> ApiStitchType:
        result = await self.stitch_type_repo.get_by_name(name)
        if result is None:
            raise NotFoundError
        return ApiStitchType(name=result.name, description=result.description)

    async def create_stitch_type(self, stitch_type: ApiStitchType) -> ApiStitchType:
        existing = await self.stitch_type_repo.get_by_name(stitch_type.name)
        if existing:
            raise AlreadyExistsError

        new_stitch_type = StitchType(
            name=stitch_type.name, description=stitch_type.description
        )
        created = await self.stitch_type_repo.create(new_stitch_type)
        await self.stitch_type_repo.commit()
        return ApiStitchType(name=created.name, description=created.description)

    async def delete_stitch_type(self, name: str) -> None:
        result = await self.stitch_type_repo.get_by_name(name)
        if result is None:
            raise NotFoundError
        await self.stitch_type_repo.delete(result)
        await self.stitch_type_repo.commit()

    async def get_relation_types(self) -> List[RelationType]:
        result = await self.relation_type_repo.get_all()
        if len(result) == 0:
            raise NotFoundError
        return result
    
    async def get_relation_type(self, name: str) -> RelationType:
        result = await self.relation_type_repo.get_by_name(name)
        if result is None:
            raise NotFoundError
        return result
    
    async def create_relation_type(self, relation_type: RelationType) -> RelationType:
        existing = await self.relation_type_repo.get_by_name(relation_type.name)
        if existing:
            raise AlreadyExistsError

        new_relation_type = RelationType(
            name=relation_type.name, description=relation_type.description
        )
        created = await self.relation_type_repo.create(new_relation_type)
        await self.relation_type_repo.commit()
        return created
    
    async def delete_relation_type(self, name: str) -> None:
        result = await self.relation_type_repo.get_by_name(name)
        if result is None:
            raise NotFoundError
        await self.relation_type_repo.delete(result)
        await self.relation_type_repo.commit()

    async def get_tool_types(self) -> List[Tool]:
        result = await self.tool_type_repo.get_all()
        if len(result) == 0:
            raise NotFoundError
        return result
    
    async def get_tool_type(self, name: str) -> Tool:
        result = await self.tool_type_repo.get_by_name(name)
        if result is None:
            raise NotFoundError
        return result
    
    async def create_tool_type(self, tool: Tool) -> Tool:
        existing = await self.tool_type_repo.get_by_name(tool.name)
        if existing:
            raise AlreadyExistsError

        new_tool = Tool(
            name=tool.name, description=tool.description
        )
        created = await self.tool_type_repo.create(new_tool)
        await self.tool_type_repo.commit()
        return created
    
    async def delete_tool_type(self, name: str) -> None:
        result = await self.tool_type_repo.get_by_name(name)
        if result is None:
            raise NotFoundError
        await self.tool_type_repo.delete(result)
        await self.tool_type_repo.commit()