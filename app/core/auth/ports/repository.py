"""
Abstract repository for user management.
"""

from abc import ABC, abstractmethod
from typing import Optional

from adapters.database.models.user_model import User


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
