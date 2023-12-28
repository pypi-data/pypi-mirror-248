"""Tokens Controller."""


from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from ..models.tokens import *
from ..schemas.tokens import *


def create_token(session: Session, user: UUID, type: TokenType) -> Token:
    """
    Creates a token.

    Parameters
    ----------
        `user` (`UUID`): the ID of the user the token belongs to

        `type` (`TokenType`): the type of the token

    Returns
    -------
        `Token`: the created token
    """
    token = TokenModel(token=uuid4(), user=user, type=type)
    session.add(token)
    session.commit()
    session.refresh(token)
    return Token(**token.as_dict())


def get_token(session: Session, token: str) -> Token:
    """
    Gets a token.

    Raises
    ------
        `HTTPException`: if the token does not exist

    Parameters
    ----------
        `token` (`str`): the token to get
    """
    return Token(**session.query(TokenModel).filter_by(token=token).one().as_dict())


def delete_token(session: Session, token: str) -> None:
    """
    Deletes a token.

    Raises
    ------
        `HTTPException`: if the token does not exist

    Parameters
    ----------
        `token` (`str`): the token to delete
    """
    session.delete(get_token(session, token))
    session.commit()
