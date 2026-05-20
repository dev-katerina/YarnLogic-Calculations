from sqlalchemy.orm import declarative_base, relationship
import uuid
from sqlalchemy import Column, LargeBinary, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from core.config import settings

Base = declarative_base()


class StitchType(Base):
    __tablename__ = f"{settings.postgres_schema}.stitch_type"

    name = Column(Text, primary_key=True)
    description = Column(Text, nullable=True)
    image = Column(LargeBinary, nullable=True)


class RelationType(Base):
    __tablename__ = f"{settings.postgres_schema}.relation_type"

    name = Column(Text, primary_key=True)
    description = Column(Text, nullable=True)


class Tool(Base):
    __tablename__ = f"{settings.postgres_schema}.tool"

    name = Column(Text, primary_key=True)
    description = Column(Text, nullable=True)

class Pattern(Base):
    __tablename__ = f"{settings.postgres_schema}.pattern"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)