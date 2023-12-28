"""Organisations Controller."""


from uuid import UUID

from sqlalchemy.orm import Session

from ..models.organisations import *
from ..schemas.organisations import *


def create_organisation(session: Session, item: OrganisationCreate) -> Organisation:
    organisation = OrganisationModel(**item.model_dump())
    session.add(organisation)
    session.commit()
    session.refresh(organisation)
    return Organisation(**organisation.as_dict())


def delete_organisation(session: Session, id: UUID) -> None:
    session.delete(get_organisation(session, id))
    session.commit()


def get_organisation(session: Session, id: UUID) -> Organisation:
    return Organisation(
        **session.query(OrganisationModel).filter_by(id=id).one().as_dict()
    )


def get_organisations(session: Session) -> list[Organisation]:
    return [
        Organisation(**organisation.as_dict())
        for organisation in session.query(OrganisationModel).all()
    ]


def update_organisation(
    session: Session, id: UUID, item: OrganisationUpdate
) -> Organisation:
    session.query(OrganisationModel).filter_by(id=id).update(
        item.model_dump(exclude_unset=True)
    )
    session.commit()

    return get_organisation(session, id)
