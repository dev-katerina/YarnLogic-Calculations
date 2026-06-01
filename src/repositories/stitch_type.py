

from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from models.postgres import StitchType
from sqlalchemy import select


class StitchTypeRepository(ABC):
        @abstractmethod
        async def get_all(self) -> List[StitchType]:
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

        async def get_all(self) -> List[StitchType]:
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