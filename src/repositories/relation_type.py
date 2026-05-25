from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from models.postgres import RelationType


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
        async def delete(self, name: str) -> None:
            pass

class RelationTypeRepositoryPostgres(RelationTypeRepository):
        def __init__(self, db: AsyncSession):
            self.db = db

        async def get_all(self) -> List[RelationType]:
            result = await self.db.query(RelationType).all()
            return result
        
        async def get_by_name(self, name: str) -> RelationType:
            result = await self.db.select(RelationType).where(RelationType.name == name)
            return result.scalar_one_or_none()
        
        async def create(self, obj: RelationType) -> None:
            self.db.add(obj)
            await self.db.flash()
            await self.db.refresh(obj)
            return obj
        
        async def update(self, obj: RelationType) -> None:
            await self.db.flash()
            await self.db.refresh(obj)
            return obj
        
        async def delete(self, name: str) -> None:
            result = await self.db.select(RelationType).where(RelationType.name == name)
            obj = result.scalar_one_or_none()
            if obj:
                await self.db.delete(obj)
                await self.db.flash()