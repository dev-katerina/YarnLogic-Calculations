

from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from elasticsearch import AsyncElasticsearch

from models.postgres import Tool
from models.es_models import ToolDocument
from sqlalchemy import select

import logging

logger = logging.getLogger(__name__)


class ToolRepository(ABC):
        @abstractmethod
        async def get_all(self) -> List[Tool]:
            pass

        @abstractmethod
        async def get_by_name(self, name: str) -> Tool:
            pass

        @abstractmethod
        async def create(self, obj: Tool) -> Tool:
            pass

        @abstractmethod
        async def update(self, obj: Tool) -> Tool:
            pass

        @abstractmethod
        async def delete(self, tool: Tool) -> None:
            pass

        @abstractmethod
        async def commit(self) -> None:
            pass

class ToolRepositoryPostgres(ToolRepository):
        def __init__(self, db: AsyncSession):
            self.db = db

        async def get_all(self) -> List[Tool]:
            result = await self.db.execute(select(Tool))
            return result.scalars().all()
        
        async def get_by_name(self, name: str) -> Tool:
            result = await self.db.execute(select(Tool).where(Tool.name == name))
            return result.scalar_one_or_none()
        
        async def create(self, obj: Tool) -> Tool:
            self.db.add(obj)
            await self.db.flush()
            await self.db.refresh(obj)
            return obj
        
        async def update(self, obj: Tool) -> Tool:
            await self.db.flush()
            await self.db.refresh(obj)
            return obj
        
        async def delete(self, tool: Tool) -> None:
            await self.db.delete(tool)
            await self.db.flush()

        async def commit(self) -> None:
            await self.db.commit()

class ToolRepositoryElastic(ToolRepository):
    def __init__(self, es_client: AsyncElasticsearch):
        self.es_client = es_client
        self.index = "tools"

    async def get_all(self) -> list[ToolDocument]:
        res = await self.es_client.search(index=self.index)

        return [
            ToolDocument.from_es(hit)
            for hit in res["hits"]["hits"]
        ]

    async def get_by_name(self, name: str) -> list[ToolDocument] | None:
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
            ToolDocument.from_es(hit)
            for hit in res["hits"]["hits"]
        ]

    async def create(self, relation: Tool) -> ToolDocument:
        tool_doc = ToolDocument(name=relation.name, description=relation.description)
        await self.es_client.index(
            index=self.index,
            document=tool_doc.to_es()
        )
        return tool_doc

    async def update(self, relation: Tool) -> ToolDocument:
        tool_doc = await self.get_by_name(relation.name)
        logger.info(f"Got rel by name {tool_doc}")
        
        if not tool_doc:
            raise ValueError("Relation not found in Elasticsearch")

        updated_doc = ToolDocument.model_validate(relation)
        await self.es_client.index(
            index=self.index,
            id=tool_doc[0]._id,
            document=updated_doc.to_es()
        )
        return updated_doc

    async def delete(self, name: str) -> None:
        tool_doc = await self.get_by_name(name)
        if not tool_doc:
            raise ValueError("Relation not found in Elasticsearch")
        try:
            await self.es_client.delete(index=self.index, id=tool_doc[0]._id)
        except Exception:
            pass

    async def commit(self):
        try:
            await self.es_client.indices.refresh(index=self.index)
        except Exception:
            pass


     