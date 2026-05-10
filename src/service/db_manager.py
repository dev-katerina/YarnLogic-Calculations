from sqlalchemy.ext.asyncio import AsyncSession
from models.postgres import RelationType, StitchType, Tool
from typing import List
from abc import ABC, abstractmethod


class ToolRepository(ABC):
    @abstractmethod
    async def get_tool_by_name(self, name: str) -> Tool:
        pass

    @abstractmethod
    async def get_tools(self) -> List[Tool]:
        pass

    @abstractmethod
    async def create_tool(self, tool: Tool) -> Tool:
        pass

    @abstractmethod
    async def delete_tool(self, name: str) -> None:
        pass


class StitchTypeRepository(ABC):
    @abstractmethod
    async def get_stitch_type_by_name(self, name: str) -> StitchType:
        pass

    @abstractmethod
    async def get_stitch_types(self) -> List[StitchType]:
        pass

    @abstractmethod
    async def create_stitch_type(self, stitch_type: StitchType) -> StitchType:
        pass

    @abstractmethod
    async def delete_stitch_type(self, name: str) -> None:
        pass


class RelationTypeRepository(ABC):
    @abstractmethod
    async def get_relation_type_by_name(self, name: str) -> RelationType:
        pass

    @abstractmethod
    async def get_relation_types(self) -> List[RelationType]:
        pass

    @abstractmethod
    async def create_relation_type(self, relation_type: RelationType) -> RelationType:
        pass

    @abstractmethod
    async def delete_relation_type(self, name: str) -> None:
        pass


class DBManager(ToolRepository, StitchTypeRepository, RelationTypeRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_tool_by_name(self, name: str):
        if not isinstance(name, str):
            raise ValueError("name должен быть строкой")
        result = await self.db.execute(
            "SELECT * FROM tool WHERE name = :name", {"name": name}
        )
        return result.fetchone()

    async def get_tools(self) -> List[Tool]:
        if not isinstance(self.db, AsyncSession):
            raise ValueError("self.db должен быть экземпляром AsyncSession")
        result = await self.db.execute("SELECT * FROM tool")
        return result.fetchall()

    async def create_tool(self, tool: Tool) -> Tool:
        if not isinstance(tool, Tool):
            raise ValueError("tool должен быть экземпляром Tool")
        self.db.add(tool)
        await self.db.commit()
        await self.db.refresh(tool)
        return tool

    async def delete_tool(self, name: str) -> None:
        if not isinstance(name, str):
            raise ValueError("name должен быть строкой")
        await self.db.execute(
            "DELETE FROM tool WHERE name = :name RETURNING *", {"name": name}
        )
        await self.db.commit()

    async def get_stitch_type_by_name(self, name: str) -> StitchType:
        if not isinstance(name, str):
            raise ValueError("name должен быть строкой")
        result = await self.db.execute(
            "SELECT * FROM stitch_type WHERE name = :name", {"name": name}
        )
        return result.fetchone()

    async def get_stitch_types(self) -> List[StitchType]:
        result = await self.db.execute("SELECT * FROM stitch_type")
        return result.fetchall()

    async def create_stitch_type(self, stitch_type: StitchType) -> StitchType:
        if not isinstance(stitch_type, StitchType):
            raise ValueError("stitch_type должен быть экземпляром StitchType")
        self.db.add(stitch_type)
        await self.db.commit()
        await self.db.refresh(stitch_type)
        return stitch_type

    async def delete_stitch_type(self, name: str) -> None:
        if not isinstance(name, str):
            raise ValueError("name должен быть строкой")
        await self.db.execute(
            "DELETE FROM stitch_type WHERE name = :name RETURNING *", {"name": name}
        )
        await self.db.commit()

    async def get_relation_type_by_name(self, name: str) -> RelationType:
        if not isinstance(name, str):
            raise ValueError("name должен быть строкой")
        result = await self.db.execute(
            "SELECT * FROM relation_type WHERE name = :name", {"name": name}
        )
        return result.fetchone()

    async def get_relation_types(self) -> List[RelationType]:
        result = await self.db.execute("SELECT * FROM relation_type")
        return result.fetchall()

    async def create_relation_type(self, relation_type: RelationType) -> RelationType:
        if not isinstance(relation_type, RelationType):
            raise ValueError("relation_type должен быть экземпляром RelationType")
        self.db.add(relation_type)
        await self.db.commit()
        await self.db.refresh(relation_type)
        return relation_type

    async def delete_relation_type(self, name: str) -> None:
        if not isinstance(name, str):
            raise ValueError("name должен быть строкой")
        await self.db.execute(
            "DELETE FROM relation_type WHERE name = :name RETURNING *", {"name": name}
        )
        await self.db.commit()
