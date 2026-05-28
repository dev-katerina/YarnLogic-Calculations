from http import HTTPStatus
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import neo4j
from uuid import UUID

from db.postgres import get_session as get_postgres_session
from db.neo4j import get_session as get_neo4j_session
from repositories import graph_manager, pattern, relation_type, stitch_type, tool_type 


from api.schemas import CreateStitch, ReadStitch
from api.schemas import CreateRelation, ReadRelation
from api.schemas import ReadPattern, CreatePattern, ReadPatternDetail

from service.patterns import PatternsService

router = APIRouter()

def get_scheduler_interval_service(
    postgres_db: AsyncSession = Depends(get_postgres_session),
    neo4j_db: neo4j.AsyncSession = Depends(get_neo4j_session),
) -> PatternsService:
    graph_repo = graph_manager.GraphManagerNeo4j(neo4j_db)
    pattern_repo = pattern.PatternRepositoryPostgres(postgres_db)
    return PatternsService(graph_repo, pattern_repo)


'''Схемы'''

@router.get(
    "",
    status_code=HTTPStatus.OK,
    response_model=List[ReadPattern],
    summary="List patterns",
    description="Return a list of all saved pattern graphs.",    
)
async def get_patterns(
    patterns: PatternsService = Depends(get_scheduler_interval_service)
):
    result =  await patterns.get_all_patterns()
    if len(result) == 0:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No patterns found")
    return result


@router.get(
    "/{graph_id}",
    status_code=HTTPStatus.OK,
    response_model=ReadPatternDetail,
    summary="Get pattern details",
    description="Return pattern metadata together with stitches and relations for the given pattern ID.",
)
async def get_pattern(graph_id: UUID, 
    patterns: PatternsService = Depends(get_scheduler_interval_service)
):
    try:
        result = await patterns.get_pattern(graph_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.post(
    "",
    status_code=HTTPStatus.CREATED,
    response_model=ReadPattern,
    summary="Create pattern",
    description="Create a new pattern graph with the provided name.",
)
async def create_pattern(pattern: CreatePattern, patterns: PatternsService = Depends(get_scheduler_interval_service)):
    new_pattern = await patterns.create_pattern(pattern)
    return new_pattern


@router.put(
    "/{graph_id}",
    status_code=HTTPStatus.OK,
    response_model=ReadPattern,
    summary="Update pattern",
    description="Update the name of an existing pattern graph by ID.",
)
async def update_pattern(graph_id: str, pattern: CreatePattern,
                         patterns: PatternsService = Depends(get_scheduler_interval_service)):
    """Update an existing pattern."""
    try:
        return await patterns.update_pattern(graph_id, pattern)
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.delete(
    "/{graph_id}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Delete pattern",
    description="Delete a pattern graph by its ID.",
)
async def delete_pattern(graph_id: str,
                         patterns: PatternsService = Depends(get_scheduler_interval_service)):
    try:
        await patterns.delete_pattern(graph_id)
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))

'''Петли'''

@router.post(
    "/{graph_id}/stitch",
    status_code=HTTPStatus.CREATED,
    response_model=ReadStitch,
    summary="Add stitch",
    description="Add a new stitch to the specified pattern graph.",
)
async def add_stitch_to_pattern(graph_id: str, stitch: CreateStitch):
    """Create a stitch within a pattern."""
    pass

@router.put(
    "/stitch/{stitch_id}",
    status_code=HTTPStatus.OK,
    response_model=ReadStitch,
    summary="Update stitch",
    description="Update an existing stitch by stitch ID.",
)
async def update_stitch_in_pattern(stitch_id: str, stitch: CreateStitch):
    """Update a stitch."""
    pass


@router.delete(
    "/stitch/{stitch_id}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Delete stitch",
    description="Remove a stitch from the pattern graph by its ID.",
)
async def delete_stitch_from_pattern(stitch_id: str):
    """Delete a stitch."""
    pass

'''Связи'''

@router.post(
    "/relation",
    status_code=HTTPStatus.CREATED,
    response_model=ReadRelation,
    summary="Add relation",
    description="Create a new relation between two stitches in a pattern.",
)
async def add_relation_to_pattern(relation: CreateRelation):
    """Create a relation."""
    pass

@router.put(
    "/relation/{relation_id}",
    status_code=HTTPStatus.OK,
    response_model=ReadRelation,
    summary="Update relation",
    description="Update an existing relation by its ID.",
)
async def update_relation_in_pattern(relation_id: str, relation: CreateRelation):
    """Update a relation."""
    pass

@router.delete(
    "/relation/{relation_id}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Delete relation",
    description="Delete a relation from the pattern graph by its ID.",
)
async def delete_relation_from_pattern(relation_id: str):
    """Delete a relation."""
    pass
