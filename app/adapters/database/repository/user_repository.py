"""
Concrete repository for user-related operations using SQLAlchemy.
"""

from typing import Optional

from adapters.database.models.user_model import User
from core.auth.ports.repository import UserRepository
from sqlalchemy.orm import Session


class SQLAlchemyUserRepository(UserRepository):
    """
    SQLAlchemy implementation of the UserRepository interface.
    """

    def __init__(self, data_base: Session):
        self.data_base = data_base

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email.

        Args:
            email (str): The user's email.

        Returns:
            Optional[User]: The user object if found, otherwise None.
        """
        return self.data_base.query(User).filter(User.email == email).first()
