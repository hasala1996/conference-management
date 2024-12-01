"""
Dependency injection for authentication services.
"""

from adapters.api.dependencies import get_db
from adapters.database.repository.user_repository import SQLAlchemyUserRepository
from core.auth.services import AuthService
from fastapi import Depends
from sqlalchemy.orm import Session


def get_user_repository(
    data_base: Session = Depends(get_db),
) -> SQLAlchemyUserRepository:
    """
    Provides an instance of `SQLAlchemyUserRepository` with its dependencies injected.

    Args:
        data_base (Session): The database session.

    Returns:
        SQLAlchemyUserRepository: The repository instance.
    """
    return SQLAlchemyUserRepository(data_base)


def get_auth_service(
    user_repository: SQLAlchemyUserRepository = Depends(get_user_repository),
) -> AuthService:
    """
    Provides an instance of `AuthService` with its dependencies injected.

    Args:
        user_repository (SQLAlchemyUserRepository): The repository instance.

    Returns:
        AuthService: The authentication service instance.
    """
    return AuthService(user_repository)
