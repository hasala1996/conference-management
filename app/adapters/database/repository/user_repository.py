"""
Concrete repository for user-related operations using SQLAlchemy.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from adapters.database.models.user_model import User
from core.auth.ports.repository import UserRepository
from core.auth.schemas import UserCreate, UserOut, UserUpdate
from core.exceptions.custom_exceptions import CustomAPIException
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

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Retrieve a user by their id.

        Args:
            id (str): The user's id.

        Returns:
            Optional[User]: The user object if found, otherwise None.
        """
        return (
            self.data_base.query(User)
            .filter(User.id == user_id, User.deleted_at.is_(None))
            .first()
        )

    def create_user(self, user_data: UserCreate) -> UserOut:
        """
        Create a new user in the database.

        Args:
            user_data (UserCreate): The data for creating the new user.

        Returns:
            UserOut: The created user object.
        """
        new_user = User(**user_data.model_dump())
        self.data_base.add(new_user)
        self.data_base.commit()
        self.data_base.refresh(new_user)
        return UserOut.model_validate(new_user)

    def update_user(self, user_id: UUID, user_data: UserUpdate) -> UserOut:
        """
        Update an existing user in the database.

        Args:
            user_id (UUID): The ID of the user to update.
            user_data (UserUpdate): The data for updating the user.

        Returns:
            UserOut: The updated user object.
        """
        user = self.data_base.query(User).filter(User.id == user_id).first()

        if not user:
            raise CustomAPIException(detail="User not found", status_code=404)

        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)

        self.data_base.commit()
        self.data_base.refresh(user)

        return UserOut.model_validate(user)

    def delete_user(self, user_id: UUID) -> None:
        user = self.data_base.query(User).filter(User.id == user_id).first()
        user.deleted_at = (
            datetime.utcnow()
        )  # Marca el campo deleted_at con la fecha actual
        self.data_base.commit()

    def list_users(self, limit: int, offset: int) -> tuple[int, list[User]]:
        """
        List paginated users.

        Args:
            limit (int): The number of users to retrieve.
            offset (int): The starting point for retrieval.

        Returns:
            tuple[int, list[User]]: The total count and list of users.
        """
        query = self.data_base.query(User).filter(User.deleted_at.is_(None))
        total_items = query.count()
        users = query.offset(offset).limit(limit).all()
        return total_items, users
