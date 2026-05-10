from sqlalchemy.orm import declarative_base, relationship
import uuid
from sqlalchemy import Column, LargeBinary, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func

Base = declarative_base()


class StitchType(Base):
    __tablename__ = "stitch_type"

    name = Column(Text, primary_key=True)
    description = Column(Text, nullable=True)
    image = Column(LargeBinary, nullable=True)


class RelationType(Base):
    __tablename__ = "relation_type"

    name = Column(Text, primary_key=True)
    description = Column(Text, nullable=True)


class Tool(Base):
    __tablename__ = "tool"

    name = Column(Text, primary_key=True)
    description = Column(Text, nullable=True)
