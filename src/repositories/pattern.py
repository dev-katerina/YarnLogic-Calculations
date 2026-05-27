from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from sqlalchemy import UUID
from models.postgres import Pattern


class PatternRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[Pattern]:
        pass

    @abstractmethod
    async def get_by_id(self, pattern_id: UUID) -> Pattern:
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> List[Pattern]|None:
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

class PatternRepositoryPostgres(PatternRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[Pattern]:
        result = await self.db.execute(select(Pattern))
        return result.scalars().all()


    async def get_by_id(self, pattern_id: UUID) -> Pattern|None:
        result = await self.db.execute(
            select(Pattern).where(Pattern.id == pattern_id)
        )
        return result.scalar_one_or_none()


    async def get_by_name(self, name: str) -> List[Pattern]|None:
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