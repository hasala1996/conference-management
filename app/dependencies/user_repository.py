"""
Dependency injection for user services and repositories.
"""

from adapters.api.dependencies import get_db
from adapters.database.repository.user_repository import SQLAlchemyUserRepository
from core.auth.user_service import UserService
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


def get_user_service(
    user_repository: SQLAlchemyUserRepository = Depends(get_user_repository),
) -> UserService:
    """
    Provides an instance of `UserService` with its dependencies injected.

    Args:
        user_repository (SQLAlchemyUserRepository): The repository instance.

    Returns:
        UserService: The user service instance.
    """
    return UserService(user_repository)
