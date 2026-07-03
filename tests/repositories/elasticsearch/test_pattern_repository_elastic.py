import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

from elasticsearch import AsyncElasticsearch
from models.postgres import Pattern
from repositories.pattern import PatternRepositoryElastic

# pytestmark = pytest.mark.elastic

@pytest.mark.asyncio
async def test_elastic_get_all(elastic_client):
    document_id = uuid4()
    repo = PatternRepositoryElastic(elastic_client)

    pattern = Pattern(id=document_id, name="Test Pattern")
    await repo.create(pattern)
    await repo.commit()

    patterns = await repo.get_all()
    assert any(p.name == "Test Pattern" for p in patterns)

@pytest.mark.asyncio
async def test_elastic_get_by_id(elastic_client):
    document_id = uuid4()
    repo = PatternRepositoryElastic(elastic_client)

    pattern = Pattern(id=document_id, name="Another Pattern")
    await repo.create(pattern)
    await repo.commit()

    fetched = await repo.get_by_id(document_id)
    assert fetched is not None
    assert fetched.id == document_id
    assert fetched.name == "Another Pattern"

@pytest.mark.asyncio
async def test_elastic_get_by_id_not_found(elastic_client):
    from uuid import uuid4
    repo = PatternRepositoryElastic(elastic_client)
    random_id = uuid4()
    pattern = await repo.get_by_id(random_id)
    assert pattern is None

@pytest.mark.asyncio
async def test_elastic_get_by_name(elastic_client):
    from uuid import uuid4
    repo = PatternRepositoryElastic(elastic_client)

    p1 = Pattern(id=uuid4(), name="First Pattern")
    p2 = Pattern(id=uuid4(), name="Second Pattern")
    await repo.create(p1)
    await repo.create(p2)
    await repo.commit()

    patterns = await repo.get_by_name("First")
    assert any(p.name == "First Pattern" for p in patterns)


@pytest.mark.asyncio
async def test_elastic_update(elastic_client):
    from uuid import uuid4
    repo = PatternRepositoryElastic(elastic_client)
    pattern = Pattern(id=uuid4(), name="Updated Pattern")
    await repo.create(pattern)
    await repo.commit()

    pattern.name = "Updated Pattern New"
    updated = await repo.update(pattern)
    await repo.commit()

    fetched = await repo.get_by_id(pattern.id)
    assert fetched is not None and fetched.name == "Updated Pattern New"

@pytest.mark.asyncio
async def test_elastic_delete(elastic_client):
    from uuid import uuid4
    repo = PatternRepositoryElastic(elastic_client)
    pattern = Pattern(id=uuid4(), name="ToDelete")
    await repo.create(pattern)
    await repo.commit()

    await repo.delete(pattern.id)
    await repo.commit()

    fetched = await repo.get_by_id(pattern.id)
    assert fetched is None


