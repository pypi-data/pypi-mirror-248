"""Authentication Router."""


from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi_another_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from ..controllers import auth as controller
from ..dependencies.database import Database
from ..schemas.auth import *
from ..schemas.users import User, UserCreate, UserPublic

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/login",
    response_model=AuthenticationToken,
    status_code=status.HTTP_200_OK,
)
def login(credentials: LoginForm = Depends(), session: Session = Depends(Database)):
    """Authenticates the user with the provided credentials."""
    return controller.login(session, credentials)


@router.post(
    "/refresh",
    response_model=AuthenticationToken,
    status_code=status.HTTP_200_OK,
)
def refresh_token(authorise: AuthJWT = Depends()):
    """Refreshes an access token."""
    return controller.refresh_token(authorise)


@router.post(
    "/sign-up",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
def sign_up(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    session: Session = Depends(Database),
):
    """Signs up a new user."""
    return controller.sign_up(session, user, background_tasks)


@router.post(
    "/verify-email",
    status_code=status.HTTP_200_OK,
)
def verify_email(token: str, session: Session = Depends(Database)):
    """Verifies a user's email address."""
    return controller.verify_email(session, token)


@router.post(
    "/forgot-password",
    status_code=status.HTTP_201_CREATED,
)
def forgot_password(
    form_data: ForgotPassword,
    background_tasks: BackgroundTasks,
    session: Session = Depends(Database),
):
    """
    Initiates the password reset process for the user specified by the given username.
    """
    return controller.forgot_password(session, form_data, background_tasks)


@router.post(
    "/reset-password",
    status_code=status.HTTP_200_OK,
)
def reset_password(
    form_data: ResetPassword, session: Session = Depends(Database)
) -> None:
    return controller.reset_password(session, form_data)


@router.get(
    "/",
    response_model=UserPublic,
    status_code=status.HTTP_200_OK,
)
def get_current_user(current_user: User = Depends(controller.get_current_user)) -> User:
    """Returns the currently authenticated user."""
    return current_user
