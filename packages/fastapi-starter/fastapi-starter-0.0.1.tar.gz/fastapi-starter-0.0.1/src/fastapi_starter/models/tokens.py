import enum

from sqlalchemy import Column, Enum, ForeignKey, String, Uuid

from . import Base

__all__ = ["TokenModel"]


class TokenType(str, enum.Enum):
    """Base model for tokens."""

    EMAIL_VERIFICATION = "EMAIL_VERIFICATION"
    """The token type for email verification."""
    PASSWORD_RESET = "PASSWORD_RESET"
    """The token type for password reset."""


class TokenModel(Base):
    """Token model."""

    __tablename__ = "tokens"

    token = Column(String(16), nullable=False, primary_key=True)
    """The token."""
    user = Column(Uuid, ForeignKey("users.id"), nullable=False)
    """The ID of the user authenticated by the token."""
    type = Column(Enum(TokenType), nullable=False)
    """The type of the token."""
