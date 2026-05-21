import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from repositories.pattern import PatternRepositoryPostgres


@pytest.fixture
def pattern_repository(mock_db):
    return PatternRepositoryPostgres(mock_db)


@pytest.mark.asyncio
async def test_get_all_executes_query(pattern_repository, mock_db):
    expected = [MagicMock(), MagicMock()]
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = expected
    mock_db.execute.return_value = mock_result

    result = await pattern_repository.get_all()

    assert result == expected
    mock_db.execute.assert_awaited_once_with("SELECT * FROM Pattern")


@pytest.mark.asyncio
async def test_get_by_id_executes_query(pattern_repository, mock_db):
    pattern_id = uuid4()
    expected = MagicMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = expected
    mock_db.execute.return_value = mock_result

    result = await pattern_repository.get_by_id(pattern_id)

    assert result is expected
    mock_db.execute.assert_awaited_once_with(
        "SELECT * FROM Pattern WHERE id = :id", {"id": pattern_id}
    )


@pytest.mark.asyncio
async def test_get_by_name_executes_query(pattern_repository, mock_db):
    name = "test_pattern"
    expected = MagicMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = expected
    mock_db.execute.return_value = mock_result

    result = await pattern_repository.get_by_name(name)

    assert result is expected
    mock_db.execute.assert_awaited_once_with(
        "SELECT * FROM Pattern WHERE name = :name", {"name": name}
    )


@pytest.mark.asyncio
async def test_create_commits_and_refreshes(pattern_repository, mock_db):
    pattern = MagicMock()

    result = await pattern_repository.create(pattern)

    mock_db.add.assert_called_once_with(pattern)
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(pattern)
    assert result is pattern


@pytest.mark.asyncio
async def test_update_commits_and_refreshes(pattern_repository, mock_db):
    pattern = MagicMock()

    result = await pattern_repository.update(pattern)

    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(pattern)
    assert result is pattern


@pytest.mark.asyncio
async def test_delete_existing_pattern_commits_and_deletes(pattern_repository, mock_db):
    pattern_id = uuid4()
    expected_pattern = MagicMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = expected_pattern
    mock_db.execute.return_value = mock_result

    await pattern_repository.delete(pattern_id)

    mock_db.execute.assert_awaited_once_with(
        "SELECT * FROM Pattern WHERE id = :id", {"id": pattern_id}
    )
    mock_db.delete.assert_awaited_once_with(expected_pattern)
    mock_db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_missing_pattern_does_not_commit(pattern_repository, mock_db):
    pattern_id = uuid4()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result

    await pattern_repository.delete(pattern_id)

    mock_db.execute.assert_awaited_once_with(
        "SELECT * FROM Pattern WHERE id = :id", {"id": pattern_id}
    )
    mock_db.delete.assert_not_awaited()
    mock_db.commit.assert_not_awaited()
