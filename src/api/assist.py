from fastapi import APIRouter

router = APIRouter()


@router.get("/stitch-types")
async def get_stitch_types():
    pass


@router.post("/stitch-types")
async def create_stitch_type():
    pass


@router.delete("/stitch-types/{name}")
async def delete_stitch_type(name: str):
    pass


@router.get("/relation-types")
async def get_relation_types():
    pass


@router.post("/relation-types")
async def create_relation_type():
    pass


@router.delete("/relation-types/{name}")
async def delete_relation_type(name: str):
    pass


@router.get("/tools")
async def get_tools():
    pass


@router.post("/tools")
async def create_tool():
    pass


@router.delete("/tools/{name}")
async def delete_tool(name: str):
    pass
