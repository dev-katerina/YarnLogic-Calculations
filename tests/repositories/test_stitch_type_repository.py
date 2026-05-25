import pytest
import asyncio
from repositories.stitch_type import StitchTypeRepositoryPostgres
from models.postgres import StitchType

@pytest.mark.asyncio
async def test_create_stitch_type(db_session):
    repo = StitchTypeRepositoryPostgres(db_session)
    data = StitchType(name="Test Stitch Type", description="A stitch type for testing")
    stitch_type = await repo.create(data)

    assert stitch_type.name == "Test Stitch Type"

@pytest.mark.asyncio
async def test_get_stitch_type_by_name(db_session):
    repo = StitchTypeRepositoryPostgres(db_session)
    data = StitchType(name="Unique Stitch Type Name")
    created_stitch_type = await repo.create(data)

    fetched_stitch_type = await repo.get_by_name("Unique Stitch Type Name")
    assert fetched_stitch_type is not None
    assert fetched_stitch_type.name == created_stitch_type.name

@pytest.mark.asyncio
async def test_update_stitch_type(db_session):
    repo = StitchTypeRepositoryPostgres(db_session)
    data = StitchType(name="Old Stitch Type Name")
    created_stitch_type = await repo.create(data)

    created_stitch_type.name = "New Stitch Type Name"
    updated_stitch_type = await repo.update(created_stitch_type)

    assert updated_stitch_type.name == "New Stitch Type Name"

@pytest.mark.asyncio
async def test_delete_stitch_type(db_session):
    repo = StitchTypeRepositoryPostgres(db_session)
    data = StitchType(name="To Be Deleted")
    created_stitch_type = await repo.create(data)

    await repo.delete(created_stitch_type.name)
    deleted_stitch_type = await repo.get_by_name(created_stitch_type.name)

    assert deleted_stitch_type is None