from pydantic import BaseModel, Field
from typing import Optional, Type, TypeVar, Any, Dict
from uuid import UUID

T = TypeVar("T", bound="ESDocument")


class ESDocument(BaseModel):
    id_doc: str | None = Field(default=None, alias="_id")

    class Config:
        from_attributes = True
        populate_by_name = True

    @property
    def _id(self) -> str | None:
        return self.id_doc

    def to_es(self) -> Dict[str, Any]:
        data = self.model_dump(exclude_none=True, exclude={"id_doc"})
        return data

    def to_es_action(self, index: str) -> Dict[str, Any]:
        return {
            "_index": index,
            "_source": self.to_es(),
        }

    @classmethod
    def from_es(cls: Type[T], hit: Dict[str, Any]) -> T:
        source = hit.get("_source", {})
        return cls(_id=hit.get("_id"), **source)
    
class StitchTypeDocument(ESDocument):
    name: str
    description: str | None = None
    image: str | None = None

class RelationTypeDocument(ESDocument):
    name: str
    description: str | None = None

class ToolDocument(ESDocument):
    name: str
    description: str | None = None

class PatternDocument(ESDocument):
    id: UUID
    name: str