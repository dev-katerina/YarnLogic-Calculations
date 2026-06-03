import pytest
import asyncio
from repositories.tool_type import ToolRepositoryPostgres
from models.postgres import Tool

@pytest.mark.asyncio
async def test_create_tool(db_session):
    repo = ToolRepositoryPostgres(db_session)
    data = Tool(name="Test Tool", description="A tool for testing")
    tool = await repo.create(data)

    assert tool.name == "Test Tool"

@pytest.mark.asyncio
async def test_get_tool_by_name(db_session):
    repo = ToolRepositoryPostgres(db_session)
    data = Tool(name="Unique Tool Name")
    created_tool = await repo.create(data)

    fetched_tool = await repo.get_by_name("Unique Tool Name")
    assert fetched_tool is not None
    assert fetched_tool.name == created_tool.name

@pytest.mark.asyncio
async def test_update_tool(db_session):
    repo = ToolRepositoryPostgres(db_session)
    data = Tool(name="Old Tool Name")
    created_tool = await repo.create(data)

    created_tool.name = "New Tool Name"
    updated_tool = await repo.update(created_tool)

    assert updated_tool.name == "New Tool Name"

@pytest.mark.asyncio
async def test_delete_tool(db_session):
    repo = ToolRepositoryPostgres(db_session)
    data = Tool(name="To Be Deleted")
    created_tool = await repo.create(data)

    await repo.delete(created_tool)
    deleted_tool = await repo.get_by_name(created_tool.name)

    assert deleted_tool is None