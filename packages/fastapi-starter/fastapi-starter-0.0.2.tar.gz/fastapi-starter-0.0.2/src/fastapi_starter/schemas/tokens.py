"""Tokens schemas."""


from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class TokenType(str, Enum):
    """Base schema for tokens."""

    EMAIL_VERIFICATION = "EMAIL_VERIFICATION"
    """The token type for email verification."""
    PASSWORD_RESET = "PASSWORD_RESET"
    """The token type for password reset."""


class TokenBase(BaseModel):
    """Base schema for tokens."""

    token: str
    """The token."""
    user: UUID
    """The ID of the user authenticated by the token."""
    type: str
    """The type of the token."""


class TokenCreate(TokenBase):
    """Creation schema for tokens."""

    pass


class Token(TokenBase):
    """Return schema for tokens."""

    pass
