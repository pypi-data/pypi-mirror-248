"""Authentication Controller."""


import re
import string
from os import getenv
from uuid import UUID

import bcrypt
from fastapi import BackgroundTasks, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_another_jwt_auth import AuthJWT
from pydantic import SecretStr
from sqlalchemy.orm import Session

from ..dependencies.database import Database
from ..models.tokens import TokenModel
from ..schemas.auth import *
from ..schemas.tokens import TokenType
from ..schemas.users import User, UserCreate, UserUpdate
from .communications import send_password_reset_email, send_welcome_email
from .tokens import create_token, delete_token, get_token
from .users import create_user, get_user, get_user_by_username, update_user

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="auth/login")
"""The OAuth2 scheme used to authenticate users."""

SECRET_KEY = getenv("SECRET_KEY")
"""The secret key used to sign JWTs."""
assert SECRET_KEY is not None

BACKGROUND_TASKS = BackgroundTasks()
"""Background tasks."""


class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_KEY


@AuthJWT.load_config
def get_config():
    return Settings()


def create_token(user_id: UUID, authorise: AuthJWT) -> AuthenticationToken:
    access_token = authorise.create_access_token(subject=str(user_id))
    refresh_token = authorise.create_refresh_token(subject=str(user_id))

    return AuthenticationToken(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=authorise._access_token_expires.total_seconds(),
        token_type="bearer",
    )


def login(session: Session, credentials: LoginForm) -> AuthenticationToken:
    """
    Authenticates a user.

    Parameters
    ----------
        `credentials` (`LoginForm`): the user's credentials

    Raises
    ------
        `HTTPException`: if the user does not exist or the password is incorrect

    Returns
    -------
        `AuthenticationToken`: the access and refresh tokens
    """
    if not (
        user := get_user_by_username(session, credentials.username)
    ) or not bcrypt.checkpw(
        credentials.password.get_secret_value().encode(),
        user.password.get_secret_value().encode(),
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return create_token(user.id, AuthJWT())


def refresh_token(authorise: AuthJWT):
    """
    Refreshes a user's access token.

    Parameters
    ----------
        `authorise` (`AuthJWT`): the user's credentials

    Raises
    ------
        `HTTPException`: if the user does not exist or the password is incorrect

    Returns
    -------
        `AuthenticationToken`: the access and refresh tokens
    """
    authorise.jwt_refresh_token_required()

    return create_token(UUID(authorise.get_jwt_subject()), authorise)


def sign_up(
    session: Session, user: UserCreate, background_tasks: BackgroundTasks
) -> User:
    """
    Registers a new user.

    Parameters
    ----------
        `user` (`UserCreate`): the user's details

        `background_tasks` (`BackgroundTasks`): background tasks

    Raises
    ------
        `HTTPException`: if a user with the given username already exists

    Returns
    -------
        `User`: the new user
    """
    if not validate_password(user.password.get_secret_value()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password",
        )

    user.password = SecretStr(
        bcrypt.hashpw(
            user.password.get_secret_value().encode(), bcrypt.gensalt()
        ).decode()
    )
    created_user = create_user(session, user)
    token = create_token(session, created_user.id, TokenType.EMAIL_VERIFICATION)
    background_tasks.add_task(send_welcome_email, created_user, token.token)

    return created_user


def verify_email(session: Session, token: str):
    """
    Verifies a user's email.

    Parameters
    ----------
        `token` (`str`): the verification token
    """
    if not (token := get_token(session, token)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
        )

    update_user(session, token.user, UserUpdate(verified=True))
    delete_token(session, token.token)


def forgot_password(
    session: Session, form_data: ForgotPassword, background_tasks: BackgroundTasks
) -> None:
    """
    Generates a password reset token and sends it to the user's email.

    Parameters
    ----------
        `form_data` (`ForgotPassword`): the user's email

        `background_tasks` (`BackgroundTasks`): background tasks
    """
    if not (user := get_user_by_username(session, form_data.email)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    for token in session.query(TokenModel).all():
        delete_token(session, token.token)

    token = create_token(session, user.id, TokenType.PASSWORD_RESET)
    background_tasks.add_task(send_password_reset_email, user, token.token)


def reset_password(session: Session, form_data: ResetPassword) -> None:
    """
    Resets a user's password.

    Parameters
    ----------
        `form_data` (`ResetPassword`): the reset token and the new password
    """
    if (
        not (token := get_token(session, form_data.token))
        or token.type != TokenType.PASSWORD_RESET
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
        )

    if not validate_password(form_data.password.get_secret_value()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password",
        )

    update_user(
        session,
        token.user,
        UserUpdate(
            password=SecretStr(
                bcrypt.hashpw(
                    form_data.password.get_secret_value().encode(), bcrypt.gensalt()
                ).decode()
            )
        ),
    )

    delete_token(session, token.token)


async def get_current_user(
    session: Session = Depends(Database),
    token: str = Depends(OAUTH2_SCHEME),
    authorise: AuthJWT = Depends(),
) -> User:
    """
    Returns the current user.

    Returns
    -------
        `User`: the current user
    """
    authorise.jwt_required()
    if not (user := get_user(session, UUID(authorise.get_jwt_subject()))):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return user


def validate_password(password: str) -> bool:
    """
    Returns whether the given string is a valid password.

    A valid password must:
        - Be at least 8 characters long
        - Contain at least one uppercase letter   (string.ascii_uppercase)
        - Contain at least one lowercase letter   (string.ascii_lowercase)
        - Contain at least one special character  (string.punctuation)
        - Contain at least one number             (string.digits)

    Parameters
    ----------
        `password` (`str`): string to validate as a password

    Returns
    -------
        `bool`: whether the string is a valid password
    """

    query = (
        "^"  # Start of string
        f"(?=.*[{string.ascii_uppercase}])"  # At least one uppercase letter
        f"(?=.*[{string.ascii_lowercase}])"  # At least one lowercase letter
        f"(?=.*[{string.punctuation}])"  # At least one special character
        f"(?=.*[{string.digits}])"  # At least one number
        ".{8,}"  # At least 8 characters long
        "$"  # End of string
    )

    return re.search(query, password) is not None
