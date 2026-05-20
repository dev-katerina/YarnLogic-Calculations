import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from repositories.pattern import PatternRepositoryPostgres


@pytest.fixture
def graph_repository(mock_db):
    return PatternRepositoryPostgres(mock_db)


@pytest.mark.asyncio
async def test_get_all_executes_query(graph_repository, mock_db):
    expected = [MagicMock(), MagicMock()]
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = expected
    mock_db.execute.return_value = mock_result

    result = await graph_repository.get_all()

    assert result == expected
    mock_db.execute.assert_awaited_once_with("SELECT * FROM Pattern")


@pytest.mark.asyncio
async def test_get_by_id_executes_query(graph_repository, mock_db):
    graph_id = uuid4()
    expected = MagicMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = expected
    mock_db.execute.return_value = mock_result

    result = await graph_repository.get_by_id(graph_id)

    assert result is expected
    mock_db.execute.assert_awaited_once_with(
        "SELECT * FROM Pattern WHERE id = :id", {"id": graph_id}
    )


@pytest.mark.asyncio
async def test_get_by_name_executes_query(graph_repository, mock_db):
    name = "test_pattern"
    expected = MagicMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = expected
    mock_db.execute.return_value = mock_result

    result = await graph_repository.get_by_name(name)

    assert result is expected
    mock_db.execute.assert_awaited_once_with(
        "SELECT * FROM Pattern WHERE name = :name", {"name": name}
    )


@pytest.mark.asyncio
async def test_create_commits_and_refreshes(graph_repository, mock_db):
    graph = MagicMock()

    result = await graph_repository.create(graph)

    mock_db.add.assert_called_once_with(graph)
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(graph)
    assert result is graph


@pytest.mark.asyncio
async def test_update_commits_and_refreshes(graph_repository, mock_db):
    graph = MagicMock()

    result = await graph_repository.update(graph)

    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(graph)
    assert result is graph


@pytest.mark.asyncio
async def test_delete_existing_graph_commits_and_deletes(graph_repository, mock_db):
    graph_id = uuid4()
    expected_graph = MagicMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = expected_graph
    mock_db.execute.return_value = mock_result

    await graph_repository.delete(graph_id)

    mock_db.execute.assert_awaited_once_with(
        "SELECT * FROM Pattern WHERE id = :id", {"id": graph_id}
    )
    mock_db.delete.assert_awaited_once_with(expected_graph)
    mock_db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_missing_graph_does_not_commit(graph_repository, mock_db):
    graph_id = uuid4()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result

    await graph_repository.delete(graph_id)

    mock_db.execute.assert_awaited_once_with(
        "SELECT * FROM Pattern WHERE id = :id", {"id": graph_id}
    )
    mock_db.delete.assert_not_awaited()
    mock_db.commit.assert_not_awaited()
