import pytest
import asyncio
from repositories.relation_type import RelationTypeRepositoryPostgres
from models.postgres import RelationType

@pytest.mark.asyncio
async def test_create_relation_type(db_session):
    repo = RelationTypeRepositoryPostgres(db_session)
    data = RelationType(name="Test Relation Type", description="A relation type for testing")
    relation_type = await repo.create(data)

    assert relation_type.name == "Test Relation Type"

@pytest.mark.asyncio
async def test_get_relation_type_by_name(db_session):
    repo = RelationTypeRepositoryPostgres(db_session)
    data = RelationType(name="Unique Relation Type Name")
    created_relation_type = await repo.create(data)

    fetched_relation_type = await repo.get_by_name("Unique Relation Type Name")
    assert fetched_relation_type is not None
    assert fetched_relation_type.name == created_relation_type.name

@pytest.mark.asyncio
async def test_update_relation_type(db_session):
    repo = RelationTypeRepositoryPostgres(db_session)
    data = RelationType(name="Old Relation Type Name")
    created_relation_type = await repo.create(data)

    created_relation_type.name = "New Relation Type Name"
    updated_relation_type = await repo.update(created_relation_type)

    assert updated_relation_type.name == "New Relation Type Name"

@pytest.mark.asyncio
async def test_delete_relation_type(db_session):
    repo = RelationTypeRepositoryPostgres(db_session)
    data = RelationType(name="To Be Deleted")
    created_relation_type = await repo.create(data)

    await repo.delete(created_relation_type)
    deleted_relation_type = await repo.get_by_name(created_relation_type.name)

    assert deleted_relation_type is None