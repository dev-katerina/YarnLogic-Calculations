from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import UUID
from models.postgres import Pattern


class PatternRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[Pattern]:
        pass

    @abstractmethod
    async def get_by_id(self, Pattern_id: UUID) -> Pattern:
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Pattern:
        pass

    @abstractmethod
    async def create(self, Pattern: Pattern):
        pass

    @abstractmethod
    async def update(self, Pattern: Pattern):
        pass

    @abstractmethod
    async def delete(self, Pattern_id: UUID):
        pass

class PatternRepositoryPostgres(PatternRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[Pattern]:
        result = await self.db.execute("SELECT * FROM Pattern")
        return result.scalars().all()
    
    async def get_by_id(self, Pattern_id: UUID) -> Pattern:
        result = await self.db.execute("SELECT * FROM Pattern WHERE id = :id", {"id": Pattern_id})
        return result.scalar_one_or_none()
    
    async def get_by_name(self, name: str) -> Pattern:
        result = await self.db.execute("SELECT * FROM Pattern WHERE name = :name", {"name": name})
        return result.scalar_one_or_none()
    
    async def create(self, Pattern: Pattern):
        self.db.add(Pattern)
        await self.db.commit()
        await self.db.refresh(Pattern)
        return Pattern
    
    async def update(self, Pattern: Pattern):
        await self.db.commit()
        await self.db.refresh(Pattern)
        return Pattern

    async def delete(self, Pattern_id: UUID):
        result = await self.db.execute("SELECT * FROM Pattern WHERE id = :id", {"id": Pattern_id})
        Pattern = result.scalar_one_or_none()
        if Pattern:
            await self.db.delete(Pattern)
            await self.db.commit()