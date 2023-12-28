from typing import Generator

from sqlalchemy.orm import Session

from ..database import session_maker


def Database() -> Generator[Session, None, None]:
    """Yields a database session."""

    session = session_maker()
    try:
        yield session
    finally:
        session.close()
