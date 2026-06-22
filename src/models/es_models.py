from pydantic import BaseModel, Field
from typing import Optional, Type, TypeVar, Any, Dict
from uuid import UUID

T = TypeVar("T", bound="ESDocument")


class ESDocument(BaseModel):
    id: str | None = Field(default=None, description="Elasticsearch _id")

    class Config:
        from_attributes = True

    def to_es(self) -> Dict[str, Any]:
        data = self.model_dump(exclude_none=True)
        data.pop("id", None)
        return data

    def to_es_action(self, index: str) -> Dict[str, Any]:
        return {
            "_index": index,
            "_id": self.id,
            "_source": self.to_es(),
        }

    @classmethod
    def from_es(cls: Type[T], hit: Dict[str, Any]) -> T:
        source = hit.get("_source", {})
        return cls(id=hit.get("_id"), **source)
    
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