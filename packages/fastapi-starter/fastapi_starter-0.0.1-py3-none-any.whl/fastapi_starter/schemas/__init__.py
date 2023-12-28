from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic import EmailStr as PydanticEmailStr
from pydantic import Field, validate_email


class HasOwner(ABC):
    """Resource which has an owner."""

    @abstractmethod
    def get_owner(self) -> UUID:
        """
        Returns the owner of the resource.

        Returns
        -------
            `UUID`: the owner of the resource
        """
        pass


class EmailStr(PydanticEmailStr):
    """Email string type."""

    @classmethod
    def validate(cls, value: PydanticEmailStr) -> PydanticEmailStr:
        email = validate_email(value)[1]
        return email.lower()


class EmailRecipient(BaseModel):
    """Email recipient schema."""

    email: EmailStr
    """The email address of the recipient."""
    first_name: str
    """The first name of the recipient."""
    last_name: str
    """The last name of the recipient."""


class InDatabase(BaseModel):
    """Resource which is in the database."""

    id: UUID
    """The ID of the resource."""
    created: datetime = Field(default_factory=datetime.utcnow)
    """When the resource was created."""


class Updatable(BaseModel):
    """Resource which is updatable."""

    updated: Optional[datetime]
    """When the resource was last updated."""
