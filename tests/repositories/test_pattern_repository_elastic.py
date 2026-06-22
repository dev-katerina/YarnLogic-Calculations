import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

from elasticsearch import AsyncElasticsearch
from models.postgres import Pattern
from repositories.pattern import PatternRepositoryElastic

pytestmark = pytest.mark.elastic

@pytest.mark.asyncio
async def test_elastic_get_all(elastic_client):
    document_id = str(uuid4())
    index_data = {
        "hits": {
            "hits": [
                {
                    "_id": document_id,
                    "_source": {
                        "name": "Test Pattern"
                    }
                }
            ]
        }
    }

    elastic_client.search = AsyncMock(return_value=index_data)

    repo = PatternRepositoryElastic(elastic_client)
    patterns = await repo.get_all()

    assert len(patterns) == 1
    assert patterns[0].id == UUID(document_id)
    assert patterns[0].name == "Test Pattern"

@pytest.mark.asyncio
async def test_elastic_get_by_id(elastic_client):
    document_id = str(uuid4())
    index_data = {
        "hits": {
            "hits": [
                {
                    "_id": document_id,
                    "_source": {
                        "name": "Another Pattern"
                    }
                }
            ]
        }
    }

    elastic_client.search = AsyncMock(return_value=index_data)

    repo = PatternRepositoryElastic(elastic_client)
    pattern = await repo.get_by_id(UUID(document_id))

    assert pattern is not None
    assert pattern.id == UUID(document_id)
    assert pattern.name == "Another Pattern"

@pytest.mark.asyncio
async def test_elastic_get_by_id_not_found(elastic_client):
    index_data = {"hits": {"hits": []}}
    elastic_client.search = AsyncMock(return_value=index_data)

    repo = PatternRepositoryElastic(elastic_client)
    pattern = await repo.get_by_id(UUID(str(uuid4())))

    assert pattern is None

@pytest.mark.asyncio
async def test_elastic_get_by_name(elastic_client):
    index_data = {
        "hits": {
            "hits": [
                {
                    "_id": str(uuid4()),
                    "_source": {
                        "name": "First Pattern"
                    }
                },
                {
                    "_id": str(uuid4()),
                    "_source": {
                        "name": "Second Pattern"
                    }
                }
            ]
        }
    }

    elastic_client.search = AsyncMock(return_value=index_data)

    repo = PatternRepositoryElastic(elastic_client)
    patterns = await repo.get_by_name("Pattern")

    assert len(patterns) == 2
    assert patterns[0].name == "First Pattern"
    assert patterns[1].name == "Second Pattern"

@pytest.mark.asyncio
async def test_elastic_create(elastic_client):
    pattern = Pattern(id=uuid4(), name="Created Pattern")
    elastic_client.index = AsyncMock(return_value={"result": "created"})

    repo = PatternRepositoryElastic(elastic_client)
    pattern_doc = await repo.create(pattern)

    assert pattern_doc.id == pattern.id
    assert pattern_doc.name == pattern.name
    elastic_client.index.assert_awaited_once_with(
        index="patterns",
        id=str(pattern.id),
        document={"name": pattern.name}
    )

@pytest.mark.asyncio
async def test_elastic_update(elastic_client):
    pattern = Pattern(id=uuid4(), name="Updated Pattern")
    elastic_client.update = AsyncMock(return_value={"result": "updated"})

    repo = PatternRepositoryElastic(elastic_client)
    pattern_doc = await repo.update(pattern)

    assert pattern_doc.id == pattern.id
    assert pattern_doc.name == pattern.name
    elastic_client.update.assert_awaited_once_with(
        index="patterns",
        id=str(pattern.id),
        doc={"name": pattern.name}
    )

@pytest.mark.asyncio
async def test_elastic_delete(elastic_client):
    pattern_id = uuid4()
    elastic_client.delete = AsyncMock(return_value={"result": "deleted"})

    repo = PatternRepositoryElastic(elastic_client)
    await repo.delete(pattern_id)

    elastic_client.delete.assert_awaited_once_with(
        index="patterns",
        id=str(pattern_id)
    )

@pytest.mark.asyncio
async def test_elastic_commit(elastic_client):
    elastic_client.indices.refresh = AsyncMock(return_value={})

    repo = PatternRepositoryElastic(elastic_client)
    await repo.commit()

    elastic_client.indices.refresh.assert_awaited_once_with(index="patterns")
