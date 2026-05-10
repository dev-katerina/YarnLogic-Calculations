import pytest
from unittest.mock import AsyncMock, MagicMock

from service.db_manager import DBManager
from models.postgres import Tool, StitchType, RelationType


@pytest.mark.asyncio
async def test_get_tool_by_name_executes_query(db_manager, mock_db):
    expected = {"name": "hook"}
    mock_result = MagicMock()
    mock_result.fetchone.return_value = expected
    mock_db.execute.return_value = mock_result

    result = await db_manager.get_tool_by_name("hook")

    assert result == expected
    mock_db.execute.assert_awaited_once_with(
        "SELECT * FROM tool WHERE name = :name",
        {"name": "hook"},
    )


@pytest.mark.asyncio
async def test_get_tools_executes_query(db_manager, mock_db):
    expected = [{"name": "hook"}, {"name": "needle"}]
    mock_result = MagicMock()
    mock_result.fetchall.return_value = expected
    mock_db.execute.return_value = mock_result

    result = await db_manager.get_tools()

    assert result == expected
    mock_db.execute.assert_awaited_once_with("SELECT * FROM tool")


@pytest.mark.asyncio
async def test_create_tool_commits_and_refreshes(db_manager, mock_db):
    tool = Tool(name="hook")

    result = await db_manager.create_tool(tool)

    mock_db.add.assert_called_once_with(tool)
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(tool)
    assert result is tool


@pytest.mark.asyncio
async def test_delete_tool_executes_delete(db_manager, mock_db):
    mock_db.execute.return_value = MagicMock()

    await db_manager.delete_tool("hook")

    mock_db.execute.assert_awaited_once_with(
        "DELETE FROM tool WHERE name = :name RETURNING *",
        {"name": "hook"},
    )
    mock_db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_stitch_type_by_name_executes_query(db_manager, mock_db):
    expected = {"name": "stockinette"}
    mock_result = MagicMock()
    mock_result.fetchone.return_value = expected
    mock_db.execute.return_value = mock_result

    result = await db_manager.get_stitch_type_by_name("stockinette")

    assert result == expected
    mock_db.execute.assert_awaited_once_with(
        "SELECT * FROM stitch_type WHERE name = :name",
        {"name": "stockinette"},
    )


@pytest.mark.asyncio
async def test_get_stitch_types_executes_query(db_manager, mock_db):
    expected = [{"name": "stockinette"}]
    mock_result = MagicMock()
    mock_result.fetchall.return_value = expected
    mock_db.execute.return_value = mock_result

    result = await db_manager.get_stitch_types()

    assert result == expected
    mock_db.execute.assert_awaited_once_with("SELECT * FROM stitch_type")


@pytest.mark.asyncio
async def test_create_stitch_type_commits_and_refreshes(db_manager, mock_db):
    stitch_type = StitchType(name="stockinette")

    result = await db_manager.create_stitch_type(stitch_type)

    mock_db.add.assert_called_once_with(stitch_type)
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(stitch_type)
    assert result is stitch_type


@pytest.mark.asyncio
async def test_delete_stitch_type_executes_delete(db_manager, mock_db):
    mock_db.execute.return_value = MagicMock()

    await db_manager.delete_stitch_type("stockinette")

    mock_db.execute.assert_awaited_once_with(
        "DELETE FROM stitch_type WHERE name = :name RETURNING *",
        {"name": "stockinette"},
    )
    mock_db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_relation_type_by_name_executes_query(db_manager, mock_db):
    expected = {"name": "friendship"}
    mock_result = MagicMock()
    mock_result.fetchone.return_value = expected
    mock_db.execute.return_value = mock_result

    result = await db_manager.get_relation_type_by_name("friendship")

    assert result == expected
    mock_db.execute.assert_awaited_once_with(
        "SELECT * FROM relation_type WHERE name = :name",
        {"name": "friendship"},
    )


@pytest.mark.asyncio
async def test_get_relation_types_executes_query(db_manager, mock_db):
    expected = [{"name": "friendship"}]
    mock_result = MagicMock()
    mock_result.fetchall.return_value = expected
    mock_db.execute.return_value = mock_result

    result = await db_manager.get_relation_types()

    assert result == expected
    mock_db.execute.assert_awaited_once_with("SELECT * FROM relation_type")


@pytest.mark.asyncio
async def test_create_relation_type_commits_and_refreshes(db_manager, mock_db):
    relation_type = RelationType(name="friendship")

    result = await db_manager.create_relation_type(relation_type)

    mock_db.add.assert_called_once_with(relation_type)
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(relation_type)
    assert result is relation_type


@pytest.mark.asyncio
async def test_delete_relation_type_executes_delete(db_manager, mock_db):
    mock_db.execute.return_value = MagicMock()

    await db_manager.delete_relation_type("friendship")

    mock_db.execute.assert_awaited_once_with(
        "DELETE FROM relation_type WHERE name = :name RETURNING *",
        {"name": "friendship"},
    )
    mock_db.commit.assert_awaited_once()
