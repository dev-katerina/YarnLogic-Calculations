from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from elasticsearch import AsyncElasticsearch

from models.postgres import RelationType
from models.es_models import RelationTypeDocument
from sqlalchemy import select

import logging

logger = logging.getLogger(__name__)

class RelationTypeRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[RelationType]:
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> RelationType:
        pass

    @abstractmethod
    async def create(self, obj: RelationType) -> None:
        pass

    @abstractmethod
    async def update(self, obj: RelationType) -> None:
        pass

    @abstractmethod
    async def delete(self, relation_type: RelationType) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

class RelationTypeRepositoryPostgres(RelationTypeRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[RelationType]:
        result = await self.db.execute(select(RelationType))
        return result.scalars().all()
    
    async def get_by_name(self, name: str) -> RelationType:
        result = await self.db.execute(select(RelationType).where(RelationType.name == name))
        return result.scalar_one_or_none()
    
    async def create(self, obj: RelationType) -> None:
        self.db.add(obj)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj
    
    async def update(self, obj: RelationType) -> None:
        await self.db.flush()
        await self.db.refresh(obj)
        return obj
    
    async def delete(self, relation_type: RelationType) -> None:
        await self.db.delete(relation_type)
        await self.db.flush()


    async def commit(self):
            return await self.db.commit()
        

class RelationTypeRepositoryElastic(RelationTypeRepository):
    def __init__(self, es_client: AsyncElasticsearch):
        self.es_client = es_client
        self.index = "relations"

    async def get_all(self) -> list[RelationTypeDocument]:
        res = await self.es_client.search(index=self.index)

        return [
            RelationTypeDocument.from_es(hit)
            for hit in res["hits"]["hits"]
        ]

    async def get_by_name(self, name: str) -> list[RelationTypeDocument] | None:
        try:
            res = await self.es_client.search(
                index=self.index,
                body={
                    "query": {
                        "match": {
                            "name": {
                                "query": name,
                                "fuzziness": "auto"
                            }
                        }
                    }
                }
            )
        except TypeError:
            res = await self.es_client.search(
                index=self.index,
                query={
                    "match": {
                        "name": {
                            "query": name,
                            "fuzziness": "auto"
                        }
                    }
                }
            )

        return [
            RelationTypeDocument.from_es(hit)
            for hit in res["hits"]["hits"]
        ]

    async def create(self, relation: RelationType) -> RelationTypeDocument:
        relation_doc = RelationTypeDocument(name=relation.name, description=relation.description)
        await self.es_client.index(
            index=self.index,
            document=relation_doc.to_es()
        )
        return relation_doc

    async def update(self, relation: RelationType) -> RelationTypeDocument:
        relation_doc = await self.get_by_name(relation.name)
        logger.info(f"Got rel by name {relation_doc}")
        
        if not relation_doc:
            raise ValueError("Relation not found in Elasticsearch")

        updated_doc = RelationTypeDocument.model_validate(relation)
        await self.es_client.index(
            index=self.index,
            id=relation_doc[0]._id,
            document=updated_doc.to_es()
        )
        return updated_doc

    async def delete(self, relation_type: RelationType) -> None:
        relation_doc = await self.get_by_name(relation_type.name)
        if not relation_doc:
            raise ValueError("Relation not found in Elasticsearch")
        try:
            await self.es_client.delete(index=self.index, id=relation_doc[0]._id)
        except Exception:
            pass

    async def commit(self):
        try:
            await self.es_client.indices.refresh(index=self.index)
        except Exception:
            pass

