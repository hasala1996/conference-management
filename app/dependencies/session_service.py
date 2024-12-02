"""
Session service dependencies.
"""

from adapters.api.dependencies import get_db
from adapters.database.repository.session_repository import SessionRepositoryImpl
from core.session.services import SessionService
from fastapi import Depends
from sqlalchemy.orm import Session


def get_session_repository(
    data_base: Session = Depends(get_db),
) -> SessionRepositoryImpl:
    """
    Provides an instance of `SessionRepositoryImpl` with its dependencies injected.

    Args:
        data_base (Session): The database session.

    Returns:
        SessionRepositoryImpl: The repository instance.
    """
    return SessionRepositoryImpl(data_base)


def get_session_service(
    session_repository: SessionRepositoryImpl = Depends(get_session_repository),
) -> SessionService:
    """
    Provides an instance of `SessionService` with its dependencies injected.

    Args:
        session_repository (SessionRepositoryImpl): The repository instance.

    Returns:
        SessionService: The session service instance.
    """
    return SessionService(session_repository)
