import pytest
from unittest.mock import AsyncMock

from elasticsearch import AsyncElasticsearch
from models.postgres import Tool
from models.es_models import ToolDocument
from repositories.tool_type import ToolRepositoryElastic

pytestmark = pytest.mark.elastic


@pytest.mark.asyncio
async def test_elastic_stitch_get_all(elastic_client):
    repo = ToolRepositoryElastic(elastic_client)
    obj = Tool(name="s1", description="d")
    await repo.create(obj)
    await repo.commit()

    items = await repo.get_all()
    assert any(i.name == "s1" or i.id == "s1" for i in items)


@pytest.mark.asyncio
async def test_elastic_stitch_get_by_name(elastic_client):
    repo = ToolRepositoryElastic(elastic_client)
    a = Tool(name="Alpha", description=None)
    b = Tool(name="Beta", description=None)
    await repo.create(a)
    await repo.create(b)
    await repo.commit()

    items = await repo.get_by_name("Alpha")
    assert any(i.name == "Alpha" for i in items)


@pytest.mark.asyncio
async def test_elastic_stitch_create_update_delete_commit(elastic_client):
    repo = ToolRepositoryElastic(elastic_client)
    obj = Tool(name="s-create5", description="desc")

    created = await repo.create(obj)
    await repo.commit()
    assert created.name == obj.name
    assert created.description == obj.description

    obj.description = "desc2"
    updated = await repo.update(obj)
    await repo.commit()
    assert updated.name == obj.name
    assert updated.description != created.description


    await repo.delete(obj.name)
    await repo.commit()

    found = await repo.get_by_name(obj.name)
    assert not any(f.name == obj.name for f in found)
