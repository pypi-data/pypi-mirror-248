import enum
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, String, Uuid, null

from . import Base

__all__ = ["OrganisationModel"]


class PermissionType(str, enum.Enum):
    ADMIN = "ADMIN"
    WRITE = "WRITE"
    READ = "READ"


class OrganisationModel(Base):
    """Organisation model."""

    __tablename__ = "organisations"

    id = Column(Uuid, default=uuid4, nullable=False, primary_key=True)
    """The ID of the organisation."""
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    """When the organisation was created."""
    updated = Column(DateTime, default=null, onupdate=datetime.utcnow)
    """When the organisation was last updated."""
    name = Column(String(50), nullable=False)
    """The name of the organisation."""
    permission = Column(Enum(PermissionType), nullable=False)
    """The permissions granted to the organisation."""
