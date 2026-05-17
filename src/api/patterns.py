from http import HTTPStatus
from typing import List
from fastapi import APIRouter
from api.schemas import CreateStitch, ReadStitch
from api.schemas import CreateRelation, ReadRelation
from api.schemas import ReadPattern, CreatePattern, ReadPatternDetail

router = APIRouter()

'''Схемы'''

@router.get("", status_code=HTTPStatus.OK, response_model=List[ReadPattern])
async def get_patterns():
    pass

@router.get(
    "/{graph_id}",
    status_code=HTTPStatus.OK,
    response_model=ReadPatternDetail,
)
async def get_pattern(graph_id: str):
    pass


@router.post("", status_code=HTTPStatus.CREATED, response_model=ReadPattern)
async def create_pattern(pattern: CreatePattern):
    pass


@router.put("/{graph_id}", status_code=HTTPStatus.OK, response_model=ReadPattern)
async def update_pattern(graph_id: str, pattern: CreatePattern):
    pass


@router.delete("/{graph_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_pattern(graph_id: str):
    pass

'''Петли'''

@router.post(
    "/{graph_id}/stitch", status_code=HTTPStatus.CREATED, response_model=ReadStitch
)
async def add_stitch_to_pattern(graph_id: str, stitch: CreateStitch):
    pass

@router.put("/stitch/{stitch_id}", status_code=HTTPStatus.OK, response_model=ReadStitch)
async def update_stitch_in_pattern(stitch_id: str, stitch: CreateStitch):
    pass


@router.delete("/stitch/{stitch_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_stitch_from_pattern(stitch_id: str):
    pass

'''Связи'''

@router.post("/relation", status_code=HTTPStatus.CREATED, response_model=ReadRelation)
async def add_relation_to_pattern(relation: CreateRelation):
    pass

@router.put("/relation/{relation_id}", status_code=HTTPStatus.OK, response_model=ReadRelation)
async def update_relation_in_pattern(relation_id: str, relation: CreateRelation):
    pass

@router.delete("/relation/{relation_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_relation_from_pattern(relation_id: str):
    pass
