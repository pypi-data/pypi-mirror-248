"""Users Schemas."""


from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, SecretStr

from . import EmailStr, InDatabase, Updatable

__all__ = ["UserCreate", "UserUpdate", "UserPublic", "User"]


class UserBase(BaseModel):
    """Base schema for users."""

    username: EmailStr
    """The username of the user."""
    first_name: str
    """The first name of the user."""
    last_name: str
    """The last name of the user."""
    organisation: UUID
    """The ID of the organisation of the user."""


class UserCreate(UserBase):
    """Creation schema for users."""

    password: SecretStr
    """The password of the user."""


class UserPublic(InDatabase, Updatable, UserBase):
    """Public return schema for users."""

    verified: Optional[bool] = Field(default=None)
    """Whether the user is verified."""

    class Config:
        from_attributes = True


class User(UserPublic):
    """Internal return schema for users."""

    password: SecretStr
    """The password of the user."""


class UserUpdate(BaseModel):
    """Modification schema for users."""

    username: Optional[EmailStr] = Field(default=None)
    """The username of the user."""
    password: Optional[SecretStr] = Field(default=None)
    """The password of the user."""
    first_name: Optional[str] = Field(default=None)
    """The first name of the user."""
    last_name: Optional[str] = Field(default=None)
    """The last name of the user."""
    organisation: Optional[UUID] = Field(default=None)
    """The ID of the organisation of the user."""
    verified: Optional[bool] = Field(default=None)
    """Whether the user is verified."""
