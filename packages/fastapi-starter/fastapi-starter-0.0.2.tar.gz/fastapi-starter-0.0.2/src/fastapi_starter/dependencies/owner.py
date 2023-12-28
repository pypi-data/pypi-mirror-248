from typing import Type
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..controllers.auth import get_current_user
from ..schemas.users import User
from .admin import Admin
from .database import Database


class Owner(Admin):
    """Requires the user to be a member of the organisation which owns the resource."""

    def __init__(
        self, database_model: Type[models.Base], return_schema: Type[schemas.HasOwner]
    ):
        """
        Initialises the Owner dependency to check for a resource of the given type in
        the given table.

        Parameters
        ----------
            `database_model` (`Type[models.Base]`): the model of the resource to check for

            `return_schema` (`Type[schemas.HasOwner]`): the type of the resource to return
        """
        self.Model = database_model
        self.Schema = return_schema

    def __call__(
        self,
        id: UUID,
        user: User = Depends(get_current_user),
        session: Session = Depends(Database),
    ) -> User:
        db_resource: self.Model = session.query(self.Model).filter_by(id=id).one()
        resource: self.Schema = self.Schema(**db_resource.as_dict())

        if resource.get_owner() == user.organisation:
            return user

        return super().__call__(user)
