

from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from models.postgres import Tool
from sqlalchemy import select


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