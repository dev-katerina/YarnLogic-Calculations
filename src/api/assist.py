from fastapi import APIRouter
from typing import List
from api.schemas import StitchType, RelationType, Tool
from http import HTTPStatus

router = APIRouter()

'''Петли'''

@router.get(
    "/stitch-type",
    response_model=List[StitchType],
    status_code=HTTPStatus.OK,
    summary="List stitch types",
    description="Return all available stitch types.",
)
async def get_stitch_types():
    """Retrieve all stitch types."""
    pass

@router.get(
    "/stitch-type/{name}",
    response_model=StitchType,
    status_code=HTTPStatus.OK,
    summary="Get stitch type",
    description="Return the details of a specific stitch type by name.",
)
async def get_stitch_type(name: str):
    """Retrieve a stitch type by name."""
    pass

@router.post(
    "/stitch-type",
    status_code=HTTPStatus.CREATED,
    response_model=StitchType,
    summary="Create stitch type",
    description="Create a new stitch type with a name and optional description.",
)
async def create_stitch_type(stitch_type: StitchType):
    """Create a new stitch type."""
    pass


@router.delete(
    "/stitch-type/{name}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Delete stitch type",
    description="Remove a stitch type by its name.",
)
async def delete_stitch_type(name: str):
    """Delete a stitch type."""
    pass

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
