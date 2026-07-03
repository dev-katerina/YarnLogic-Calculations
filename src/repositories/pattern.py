from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from elasticsearch import AsyncElasticsearch

from sqlalchemy import select
from sqlalchemy import UUID

from models.postgres import Pattern
from models.es_models import PatternDocument

import logging

logger = logging.getLogger(__name__)


class PatternRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[Pattern]:
        pass

    @abstractmethod
    async def get_by_id(self, pattern_id: UUID) -> Pattern:
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> list[Pattern]|None:
        pass

    @abstractmethod
    async def create(self, pattern: Pattern) -> Pattern:
        pass

    @abstractmethod
    async def update(self, pattern: Pattern) -> Pattern:
        pass

    @abstractmethod
    async def delete(self, pattern_id: UUID):
        pass

    @abstractmethod
    async def commit(self):
        pass

class PatternRepositoryPostgres(PatternRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Pattern]:
        result = await self.db.execute(select(Pattern))
        return result.scalars().all()


    async def get_by_id(self, pattern_id: UUID) -> Pattern|None:
        result = await self.db.execute(
            select(Pattern).where(Pattern.id == pattern_id)
        )
        return result.scalar_one_or_none()


    async def get_by_name(self, name: str) -> list[Pattern]|None:
        result = await self.db.execute(
            select(Pattern).where(Pattern.name == name)
        )
        return result.scalars().all()
    
    async def create(self, pattern: Pattern) -> Pattern:
        self.db.add(pattern)
        await self.db.flush()
        await self.db.refresh(pattern)
        return pattern
    
    async def update(self, pattern: Pattern) -> Pattern:
        await self.db.flush()
        await self.db.refresh(pattern)
        return pattern

    async def delete(self, pattern_id: UUID):
        stmt = select(Pattern).where(Pattern.id == pattern_id)
        result = await self.db.execute(stmt)

        obj = result.scalar_one_or_none()

        if obj:
            await self.db.delete(obj)
            await self.db.flush()

    async def commit(self):
        await self.db.commit()


class PatternRepositoryElastic(PatternRepository):
    def __init__(self, db: AsyncElasticsearch):
        self.db = db
        self.index = "graphs"

    async def get_all(self) -> list[PatternDocument]:
        res = await self.db.search(index=self.index)

        return [
            PatternDocument.from_es(hit)
            for hit in res["hits"]["hits"]
        ]

    async def get_by_id(self, pattern_id: UUID) -> PatternDocument | None:
        res = await self.db.search(
            index=self.index,
            query={
                "term": {
                    "id": str(pattern_id)  # Преобразуем UUID в строку
                }
            }
        )
        hits = res["hits"]["hits"]
        if not hits:
            return None
        return PatternDocument.from_es(hits[0])
    
    async def get_by_name(self, name: str) -> list[PatternDocument] | None:
        res = await self.db.search(
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
        return [
            PatternDocument.from_es(hit)
            for hit in res["hits"]["hits"]
        ]

    async def create(self, pattern: Pattern) -> PatternDocument:
        pattern_doc = PatternDocument(id=pattern.id, name=pattern.name)
        await self.db.index(
            index=self.index,
            document=pattern_doc.to_es()
        )
        logger.info(f"Created pattern {pattern_doc}")
        return pattern_doc

    async def update(self, pattern: Pattern) -> PatternDocument:
        pattern_doc = await self.get_by_id(pattern.id)
        if not pattern_doc:
            raise ValueError("Pattern not found in Elasticsearch")
        
        pattern_changed = PatternDocument.model_validate(pattern)

        await self.db.update(
            index=self.index,
            id=str(pattern_doc._id),
            doc=pattern_changed.to_es()
        )
        return pattern_doc

    async def delete(self, pattern_id: UUID):
        pattern_doc = await self.get_by_id(pattern_id)
        if not pattern_doc:
            raise ValueError("Pattern not found in Elasticsearch")
        
        await self.db.delete(
            index=self.index,
            id=str(pattern_doc._id)
        )

    async def commit(self):
        try:
            await self.db.indices.refresh(index=self.index)
        except Exception:
            pass
