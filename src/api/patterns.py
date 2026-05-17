from http import HTTPStatus
from typing import List
from fastapi import APIRouter
from api.schemas import CreateStitch, ReadStitch
from api.schemas import CreateRelation, ReadRelation
from api.schemas import ReadPattern, CreatePattern, ReadPatternDetail

router = APIRouter()

'''Схемы'''

@router.get(
    "",
    status_code=HTTPStatus.OK,
    response_model=List[ReadPattern],
    summary="List patterns",
    description="Return a list of all saved pattern graphs.",
)
async def get_patterns():
    """Retrieve all registered patterns."""
    pass

@router.get(
    "/{graph_id}",
    status_code=HTTPStatus.OK,
    response_model=ReadPatternDetail,
    summary="Get pattern details",
    description="Return pattern metadata together with stitches and relations for the given pattern ID.",
)
async def get_pattern(graph_id: str):
    """Retrieve a pattern with its stitches and relations."""
    pass


@router.post(
    "",
    status_code=HTTPStatus.CREATED,
    response_model=ReadPattern,
    summary="Create pattern",
    description="Create a new pattern graph with the provided name.",
)
async def create_pattern(pattern: CreatePattern):
    """Create a new pattern."""
    pass


@router.put(
    "/{graph_id}",
    status_code=HTTPStatus.OK,
    response_model=ReadPattern,
    summary="Update pattern",
    description="Update the name of an existing pattern graph by ID.",
)
async def update_pattern(graph_id: str, pattern: CreatePattern):
    """Update an existing pattern."""
    pass


@router.delete(
    "/{graph_id}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Delete pattern",
    description="Delete a pattern graph by its ID.",
)
async def delete_pattern(graph_id: str):
    """Delete a pattern."""
    pass

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
