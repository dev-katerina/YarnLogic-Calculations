import pytest
import asyncio
from repositories.pattern import PatternRepositoryPostgres
from models.postgres import Pattern

@pytest.mark.asyncio
async def test_create_pattern(db_session):
    repo = PatternRepositoryPostgres(db_session)
    data = Pattern(name="Test Pattern")
    pattern = await repo.create(data)

    assert pattern.id is not None

@pytest.mark.asyncio
async def test_get_pattern_by_id(db_session):
    repo = PatternRepositoryPostgres(db_session)
    data = Pattern(name="Test Pattern")
    created_pattern = await repo.create(data)

    fetched_pattern = await repo.get_by_id(created_pattern.id)
    assert fetched_pattern is not None
    assert fetched_pattern.id == created_pattern.id    

@pytest.mark.asyncio
async def test_get_pattern_by_name(db_session):
    repo = PatternRepositoryPostgres(db_session)
    data = Pattern(name="Unique Pattern Name")
    created_pattern = await repo.create(data)

    fetched_pattern = await repo.get_by_name("Unique Pattern Name")
    assert fetched_pattern is not None
    assert fetched_pattern[0].id == created_pattern.id

@pytest.mark.asyncio
async def test_update_pattern(db_session):
    repo = PatternRepositoryPostgres(db_session)
    data = Pattern(name="Old Name")
    created_pattern = await repo.create(data)

    created_pattern.name = "New Name"
    updated_pattern = await repo.update(created_pattern)

    assert updated_pattern.name == "New Name"

@pytest.mark.asyncio
async def test_delete_pattern(db_session):
    repo = PatternRepositoryPostgres(db_session)
    data = Pattern(name="To Be Deleted")
    created_pattern = await repo.create(data)

    await repo.delete(created_pattern.id)
    deleted_pattern = await repo.get_by_id(created_pattern.id)

    assert deleted_pattern is None