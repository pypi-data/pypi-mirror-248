from fastapi import HTTPException, status

from ..controllers.organisations import get_organisation
from ..schemas.organisations import PermissionType
from ..schemas.users import User


class Admin:
    """
    Requires the user to be a member of an organisation with administrative permissions.
    """

    def __call__(self, user: User) -> User:
        organisation = get_organisation(user.organisation)

        if organisation.permission == PermissionType.ADMIN:
            return user

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
