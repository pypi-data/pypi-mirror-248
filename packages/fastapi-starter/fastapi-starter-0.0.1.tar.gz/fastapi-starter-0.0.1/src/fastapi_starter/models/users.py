from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Uuid, null

from . import Base

__all__ = ["UserModel"]


class UserModel(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Uuid, nullable=False, default=uuid4, primary_key=True)
    """The ID of the user."""
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    """When the user was created."""
    updated = Column(DateTime, default=null, onupdate=datetime.utcnow)
    """When the user was last updated."""
    username = Column(String(30), unique=True, nullable=False)
    """The username of the user."""
    password = Column(String(60), nullable=False)
    """The password of the user."""
    first_name = Column(String(20), nullable=False)
    """The first name of the user."""
    last_name = Column(String(20), nullable=False)
    """The last name of the user."""
    organisation = Column(Uuid, ForeignKey("organisations.id"), nullable=False)
    """The ID of the organisation of the user."""
    verified = Column(Boolean, nullable=False, default=False)
    """Whether the user is verified."""
