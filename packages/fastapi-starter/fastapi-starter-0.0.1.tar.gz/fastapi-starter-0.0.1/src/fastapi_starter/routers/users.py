"""Users Router."""


from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..controllers import users as controller
from ..controllers.auth import get_current_user
from ..dependencies.database import Database
from ..dependencies.self import Self
from ..schemas.users import *

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "/",
    response_model=list[UserPublic],
)
def get_users(session: Session = Depends(Database)):
    """Returns all users."""
    return controller.get_users(session)


@router.get(
    "/{id}",
    dependencies=[Depends(Self)],
    response_model=UserPublic,
)
def get_user(id: UUID, session: Session = Depends(Database)):
    """Returns the user specified by the given ID."""
    return controller.get_user(session, id)


@router.put(
    "/{id}",
    dependencies=[Depends(Self)],
    response_model=UserPublic,
)
def update_user(id: UUID, item: UserUpdate, session: Session = Depends(Database)):
    """Updates the user specified by the given ID."""
    return controller.update_user(session, id, item)


@router.delete(
    "/{id}",
    dependencies=[Depends(Self)],
)
def delete_user(id: UUID, session: Session = Depends(Database)):
    """Deletes the user specified by the given ID."""
    return controller.delete_user(session, id)
