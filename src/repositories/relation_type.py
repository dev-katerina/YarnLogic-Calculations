from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from models.postgres import RelationType
from sqlalchemy import select


class RelationTypeRepository(ABC):
        @abstractmethod
        async def get_all(self) -> List[RelationType]:
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

        async def get_all(self) -> List[RelationType]:
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