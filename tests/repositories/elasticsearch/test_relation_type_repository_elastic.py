import pytest
from unittest.mock import AsyncMock

from elasticsearch import AsyncElasticsearch
from models.postgres import RelationType
from repositories.relation_type import RelationTypeRepositoryElastic

# pytestmark = pytest.mark.elastic


@pytest.mark.asyncio
async def test_elastic_relation_get_all(elastic_client):
    repo = RelationTypeRepositoryElastic(elastic_client)
    rel = RelationType(name="rel1", description="d1")
    await repo.create(rel)
    await repo.commit()

    items = await repo.get_all()
    assert any(i.name == "rel1" or i.id == "rel1" for i in items)


@pytest.mark.asyncio
async def test_elastic_relation_get_by_name(elastic_client):
    repo = RelationTypeRepositoryElastic(elastic_client)
    r1 = RelationType(name="Alpha", description="a")
    r2 = RelationType(name="Beta", description="b")
    await repo.create(r1)
    await repo.create(r2)
    await repo.commit()

    items = await repo.get_by_name("Alpha")
    assert any(i.name == "Alpha" for i in items)


@pytest.mark.asyncio
async def test_elastic_relation_create_update_delete_commit(elastic_client):
    repo = RelationTypeRepositoryElastic(elastic_client)
    rel = RelationType(name="rel-create7", description="desc")

    created = await repo.create(rel)
    await repo.commit()
    assert created.name == rel.name
    assert created.name == rel.name

    # update
    rel.description = "desc2"
    updated = await repo.update(rel)
    await repo.commit()
    assert updated.name == rel.name

    await repo.delete(rel)
    await repo.commit()

    found = await repo.get_by_name(rel.name)
    # after delete, search should not return the same name
    assert not any(f.name == rel.name for f in found)
