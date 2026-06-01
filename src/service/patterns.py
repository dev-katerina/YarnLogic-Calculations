from typing import List
from uuid import uuid4

from repositories import graph_manager, pattern, relation_type, stitch_type, tool_type
from models.postgres import Pattern, RelationType, StitchType, Tool
from models.neo4j import Stitch , Relation
from api.schemas import (
    CreatePattern,
    ReadPattern,
    CreateStitch,
    ReadPatternDetail,
    ReadStitch,
    CreateRelation,
    ReadRelation,
)


class PatternsService:
    def __init__(
        self,
        graph_repo: graph_manager.GraphManager,
        pattern_repo: pattern.PatternRepository,
        stitch_type_repo: stitch_type.StitchTypeRepository,
        relation_type_repo: relation_type.RelationTypeRepository,
        tool_type_repo: tool_type.ToolRepository,
    ):
        self.graph_repo = graph_repo
        self.pattern_repo = pattern_repo
        self.stitch_type_repo = stitch_type_repo
        self.relation_type_repo = relation_type_repo
        self.tool_type_repo = tool_type_repo

    async def get_all_patterns(self) -> List[ReadPattern]:
        patterns = await self.pattern_repo.get_all()
        return [ReadPattern(graph_id=str(p.id), name=p.name) for p in patterns]

    async def get_pattern(self, pattern_id) -> ReadPatternDetail:
        pattern_info = await self.pattern_repo.get_by_id(pattern_id)
        if not pattern_info:
            raise ValueError("Pattern not found")
        
        graph_data = await self.graph_repo.query_graph(pattern_id)
        stitches = []
        relations = []
        for stitch_node, relation, target_node in graph_data:
            stitches.append(
                ReadStitch(
                    id=str(stitch_node.id),
                    type=stitch_node.type,
                    tool=stitch_node.tool,
                    graph_id=str(pattern_id),
                )
            )
            relations.append(
                ReadRelation(
                    id=str(relation.id),
                    type=relation.type,
                    graph_id=str(pattern_id),
                    base_stitch_id=str(stitch_node.id),
                    target_stitch_id=str(target_node.id),
                )
            )
        return ReadPatternDetail(
            pattern=ReadPattern(graph_id=str(pattern_id), name=pattern_info.name),
            stitches=list(set(stitches)),
            relations=relations,
        )

    async def create_pattern(self, pattern_data: CreatePattern) -> ReadPattern:
        new_pattern = await self.pattern_repo.create(Pattern(name=pattern_data.name))
        await self.pattern_repo.commit()
        return ReadPattern(graph_id=str(new_pattern.id), name=new_pattern.name)
    
    async def update_pattern(self, pattern_id: str, pattern_data: CreatePattern) -> ReadPattern:
        pattern_obj = await self.pattern_repo.get_by_id(pattern_id)

        if not pattern_obj:
            raise ValueError("Pattern not found")
        
        pattern_obj.name = pattern_data.name
        updated_pattern = await self.pattern_repo.update(pattern_obj)
        await self.pattern_repo.commit()

        return ReadPattern(graph_id=str(updated_pattern.id), name=updated_pattern.name)
    
    async def delete_pattern(self, pattern_id: str):
        pattern_obj = await self.pattern_repo.get_by_id(pattern_id)  # Проверяем, что паттерн существует

        if not pattern_obj:
            raise ValueError("Pattern not found")

        await self.graph_repo.delete_graph(pattern_id)
        await self.pattern_repo.delete(pattern_id)
        await self.pattern_repo.commit()

    async def add_stitch(self, graph_id: str, stitch: CreateStitch):
        pattern_info = await self.pattern_repo.get_by_id(graph_id)
        if not pattern_info:
            raise ValueError("Pattern not found")
        
        type_info = await self.stitch_type_repo.get_by_name(stitch.type)
        if not type_info:
            raise ValueError("Stitch type not found")
        
        tool_info = await self.tool_type_repo.get_by_name(stitch.tool)
        if not tool_info:
            raise ValueError("Tool type not found")

        stitch_id = uuid4()
        
        while await self.graph_repo.get_node(stitch_id) is not None:
            stitch_id = uuid4()  # Генерируем новый UUID, если уже существует

        new_stitch = Stitch(id=uuid4(), 
                            type=stitch.type, 
                            tool=stitch.tool, 
                            graph_id=graph_id)
        self.graph_repo.add_node(new_stitch)