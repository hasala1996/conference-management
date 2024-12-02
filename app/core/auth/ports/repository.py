"""
Abstract repository for user management.
"""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from adapters.database.models.user_model import User
from core.auth.schemas import UserCreate, UserOut, UserUpdate


class UserRepository(ABC):
    """
    Abstract repository for user-related operations.
    """

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email.

        Args:
            email (str): The user's email.

        Returns:
            Optional[User]: The user object if found, otherwise None.
        """

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Retrieve a user by their id.

        Args:
            id (str): The user's id.

        Returns:
            Optional[User]: The user object if found, otherwise None.
        """

    @abstractmethod
    def create_user(self, user_data: UserCreate) -> UserOut:
        """
        Create a new user in the system.
        """

    @abstractmethod
    def update_user(self, user_id: UUID, user_data: UserUpdate) -> UserOut:
        """
        Update an existing user's information.
        """

    @abstractmethod
    def delete_user(self, user_id: UUID) -> None:
        """
        Delete (or deactivate) a user by their ID.
        """

    @abstractmethod
    def list_users(self, limit: int, offset: int) -> tuple[int, list[User]]:
        """
        List paginated users.

        Args:
            limit (int): The number of users to retrieve.
            offset (int): The starting point for retrieval.

        Returns:
            tuple[int, list[User]]: The total count and list of users.
        """
