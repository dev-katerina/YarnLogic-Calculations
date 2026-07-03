

from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from elasticsearch import AsyncElasticsearch

from models.postgres import StitchType
from models.es_models import StitchTypeDocument

from sqlalchemy import select



class StitchTypeRepository(ABC):
        @abstractmethod
        async def get_all(self) -> list[StitchType]:
            pass

        @abstractmethod
        async def get_by_name(self, name: str) -> StitchType|None:
            pass

        @abstractmethod
        async def create(self, obj: StitchType) -> None:
            pass

        @abstractmethod
        async def update(self, obj: StitchType) -> None:
            pass

        @abstractmethod
        async def delete(self, name: str) -> None:
            pass

        @abstractmethod
        async def commit(self) -> None:
            pass

class StitchTypeRepositoryPostgres(StitchTypeRepository):
        def __init__(self, db: AsyncSession):
            self.db = db

        async def get_all(self) -> list[StitchType]:
            result = await self.db.execute(select(StitchType))
            return result.scalars().all()
        
        async def get_by_name(self, name: str) -> StitchType|None:
            result = await self.db.execute(select(StitchType).where(StitchType.name == name))
            return result.scalar_one_or_none()
        
        async def create(self, obj: StitchType) -> None:
            self.db.add(obj)
            await self.db.flush()
            await self.db.refresh(obj)
            return obj
        
        async def update(self, obj: StitchType) -> None:
            await self.db.flush()
            await self.db.refresh(obj)
            return obj
        
        async def delete(self, stitch_type: StitchType) -> None:
            await self.db.delete(stitch_type)
            await self.db.flush()

        async def commit(self):
             return await self.db.commit()


class StitchTypeRepositoryElastic(StitchTypeRepository):
        def __init__(self, db: AsyncElasticsearch):
            self.db = db
            self.index = "stitches"

        async def get_all(self) -> list[StitchTypeDocument]:
            res = await self.db.search(index=self.index)

            return [
                StitchTypeDocument.from_es(hit)
                for hit in res["hits"]["hits"]
            ]

        async def get_by_name(self, name: str) -> list[StitchTypeDocument] | None:
            try:
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
            except TypeError:
                res = await self.db.search(
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
                StitchTypeDocument.from_es(hit)
                for hit in res["hits"]["hits"]
            ]
        async def create(self, obj: StitchType) -> StitchTypeDocument:
            doc = StitchTypeDocument(id=obj.name, name=obj.name, description=obj.description, image=None)
            await self.db.index(index=self.index, document=doc.to_es())
            return doc

        async def update(self, obj: StitchType) -> StitchTypeDocument:
            stitch_doc = await self.get_by_name(obj.name)
            if not stitch_doc:
                raise ValueError("Relation not found in Elasticsearch")
            
            updated_doc = StitchTypeDocument(name=obj.name, description=obj.description, image=obj.image)
            await self.db.index(
                index=self.index,
                id=stitch_doc[0]._id,
                document=updated_doc.to_es()
            )
            return updated_doc

        async def delete(self, name: str) -> None:
            stitch_doc = await self.get_by_name(name)
            if not stitch_doc:
                raise ValueError("Relation not found in Elasticsearch")
            try:
                await self.db.delete(index=self.index, id=stitch_doc[0]._id)
            except Exception:
                pass

        async def commit(self):
            try:
                await self.db.indices.refresh(index=self.index)
            except Exception:
                pass