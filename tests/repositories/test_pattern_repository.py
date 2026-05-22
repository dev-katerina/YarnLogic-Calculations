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