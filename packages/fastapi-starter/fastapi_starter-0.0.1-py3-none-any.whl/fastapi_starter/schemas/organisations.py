"""Organisations Schemas."""


from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from . import HasOwner, InDatabase, Updatable

__all__ = ["OrganisationCreate", "OrganisationUpdate", "Organisation"]


class PermissionType(str, Enum):
    ADMIN = "ADMIN"
    WRITE = "WRITE"
    READ = "READ"


class OrganisationBase(BaseModel):
    """Base schema for organisations."""

    name: str
    """The name of the organisation."""
    permission: PermissionType
    """The permissions granted to the organisation."""


class OrganisationCreate(OrganisationBase):
    """Creation schema for organisations."""

    pass


class Organisation(HasOwner, InDatabase, Updatable, OrganisationBase):
    """Return schema for organisations."""

    def get_owner(self):
        return self.id

    class Config:
        from_attributes = True


class OrganisationUpdate(BaseModel):
    """Modification schema for organisations."""

    name: Optional[str] = Field(default=None)
    """The name of the organisation."""
    permission: Optional[PermissionType] = Field(default=None)
    """The permissions granted to the organisation."""
