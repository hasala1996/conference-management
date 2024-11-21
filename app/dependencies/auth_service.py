"""
Dependency injection for authentication services.
"""

from adapters.api.dependencies import get_db
from adapters.database.repository.user_repository import SQLAlchemyUserRepository
from core.auth.services import AuthService
from fastapi import Depends
from sqlalchemy.orm import Session


def get_auth_service(data_base: Session = Depends(get_db)) -> AuthService:
    """
    Provides an instance of `AuthService` with its dependencies injected.

    Args:
        db (Session): The database session.

    Returns:
        AuthService: The authentication service instance.
    """
    user_repository = SQLAlchemyUserRepository(data_base)
    return AuthService(user_repository)
