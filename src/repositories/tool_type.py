

from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from models.postgres import Tool


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
        async def delete(self, name: str) -> None:
            pass

class ToolRepositoryPostgres(ToolRepository):
        def __init__(self, db: AsyncSession):
            self.db = db

        async def get_all(self) -> List[Tool]:
            result = await self.db.query(Tool).all()
            return result
        
        async def get_by_name(self, name: str) -> Tool:
            result = await self.db.select(Tool).where(Tool.name == name)
            return result.scalar_one_or_none()
        
        async def create(self, obj: Tool) -> Tool:
            self.db.add(obj)
            await self.db.flash()
            await self.db.refresh(obj)
            return obj
        
        async def update(self, obj: Tool) -> Tool:
            await self.db.flash()
            await self.db.refresh(obj)
            return obj
        
        async def delete(self, name: str) -> None:
            result = await self.db.select(Tool).where(Tool.name == name)
            obj = result.scalar_one_or_none()
            if obj:
                await self.db.delete(obj)
                await self.db.flash()