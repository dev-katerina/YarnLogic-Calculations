from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from api.schemas import StitchType, RelationType, Tool
from http import HTTPStatus

from db.postgres import get_session as get_postgres_session
from repositories import pattern, relation_type, stitch_type, tool_type 

from core.errors import NotFoundError, AlreadyExistsError

from service.assist import AssistService

router = APIRouter()


def get_assist_service(
    postgres_db: AsyncSession = Depends(get_postgres_session),
) -> AssistService:
    pattern_repo = pattern.PatternRepositoryPostgres(postgres_db)
    stitch_type_repo = stitch_type.StitchTypeRepositoryPostgres(postgres_db)
    relation_type_repo = relation_type.RelationTypeRepositoryPostgres(postgres_db)
    tool_type_repo = tool_type.ToolRepositoryPostgres(postgres_db)
    return AssistService(pattern_repo, stitch_type_repo, relation_type_repo, tool_type_repo)

'''Петли'''

@router.get(
    "/stitch-type",
    response_model=List[StitchType],
    status_code=HTTPStatus.OK,
    summary="List stitch types",
    description="Return all available stitch types.",
)
async def get_stitch_types(
    assist: AssistService = Depends(get_assist_service)
):
    try:
        return await assist.get_stitch_types()
    except NotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=NotFoundError.INVALID_PARAMETERS)

@router.get(
    "/stitch-type/{name}",
    response_model=StitchType,
    status_code=HTTPStatus.OK,
    summary="Get stitch type",
    description="Return the details of a specific stitch type by name.",
)
async def get_stitch_type(name: str,
    assist: AssistService = Depends(get_assist_service)):
    """Retrieve a stitch type by name."""
    try:
        return await assist.get_stitch_type(name)
    except NotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=NotFoundError.INVALID_PARAMETERS)

@router.post(
    "/stitch-type",
    status_code=HTTPStatus.CREATED,
    response_model=StitchType,
    summary="Create stitch type",
    description="Create a new stitch type with a name and optional description.",
)
async def create_stitch_type(stitch_type: StitchType,
    assist: AssistService = Depends(get_assist_service)):
    try:
        return await assist.create_stitch_type(stitch_type)
    except AlreadyExistsError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=AlreadyExistsError.INVALID_PARAMETERS)



@router.delete(
    "/stitch-type/{name}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Delete stitch type",
    description="Remove a stitch type by its name.",
)
async def delete_stitch_type(name: str,
    assist: AssistService = Depends(get_assist_service)):
    """Delete a stitch type."""
    try:
        await assist.delete_stitch_type(name)
    except NotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=NotFoundError.INVALID_PARAMETERS)

'''Связи'''

@router.get(
    "/relation-types",
    response_model=List[RelationType],
    status_code=HTTPStatus.OK,
    summary="List relation types",
    description="Return all available relation types.",
)
async def get_relation_types():
    """Retrieve all relation types."""
    pass

@router.get(
    "/relation-types/{name}",
    response_model=RelationType,
    status_code=HTTPStatus.OK,
    summary="Get relation type",
    description="Return the details of a specific relation type by name.",
)
async def get_relation_type(name: str):
    """Retrieve a relation type by name."""
    pass

@router.post(
    "/relation-types",
    status_code=HTTPStatus.CREATED,
    response_model=RelationType,
    summary="Create relation type",
    description="Create a new relation type with a name and optional description.",
)
async def create_relation_type(relation_type: RelationType):
    """Create a new relation type."""
    pass


@router.delete(
    "/relation-types/{name}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Delete relation type",
    description="Remove a relation type by its name.",
)
async def delete_relation_type(name: str):
    """Delete a relation type."""
    pass

'''Инструменты'''

@router.get(
    "/tools",
    response_model=List[Tool],
    status_code=HTTPStatus.OK,
    summary="List tools",
    description="Return all available tools.",
)
async def get_tools():
    """Retrieve all tools."""
    pass

@router.get(
    "/tools/{name}",
    response_model=Tool,
    status_code=HTTPStatus.OK,
    summary="Get tool",
    description="Return the details of a specific tool by name.",
)
async def get_tool(name: str):  
    """Retrieve a tool by name."""
    pass

@router.post(
    "/tools",
    status_code=HTTPStatus.CREATED,
    response_model=Tool,
    summary="Create tool",
    description="Create a new tool with a name and optional description.",
)
async def create_tool(tool: Tool):
    """Create a new tool."""
    pass


@router.delete(
    "/tools/{name}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Delete tool",
    description="Remove a tool by its name.",
)
async def delete_tool(name: str):
    """Delete a tool."""
    pass
