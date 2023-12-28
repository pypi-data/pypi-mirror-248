from uuid import UUID

from ..schemas.users import User
from .admin import Admin


class Self(Admin):
    """Requires the user to be the resource."""

    def __call__(self, user: User, id: UUID) -> User:
        if user.id == id:
            return user

        return super().__call__(user)
