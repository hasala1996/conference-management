from core.auth.ports.repository import UserRepository
from core.auth.schemas import UserCreate, UserDetail, UserOut, UserUpdate
from core.common.pagination import Paginated, PaginatedResponse, PaginationParams
from core.exceptions.custom_exceptions import CustomAPIException
from passlib.hash import bcrypt


class UserService:
    """
    Service for managing users and their business logic.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Initialize the UserService with a repository.

        Args:
            user_repository (UserRepository): The repository to interact with user data.
        """
        self.user_repository = user_repository

    def get_user(self, user_id):
        """
        Retrieve a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The retrieved user object.
        """
        return self.user_repository.get_user_by_id(user_id)

    def hash_password(self, password: str) -> str:
        """
        Hash a plaintext password.

        Args:
            password (str): The plaintext password.

        Returns:
            str: The hashed password.
        """
        return bcrypt.hash(password)

    def create_user(self, user_data: UserCreate) -> UserOut:
        """
        Create a new user.

        Args:
            user_data (UserCreate): The data for creating the new user.

        Returns:
            UserOut: The created user object.
        """
        user_data.password = self.hash_password(user_data.password)

        return self.user_repository.create_user(user_data)

    def update_user(self, user_id: str, user_data: UserUpdate) -> UserOut:
        """
        Update an existing user.

        Args:
            user_id (str): The ID of the user to update.
            user_data (UserUpdate): The data for updating the user.

        Returns:
            UserOut: The updated user object.
        """
        if user_data.password:
            user_data.password = self.hash_password(user_data.password)

        return self.user_repository.update_user(user_id, user_data)

    def delete_user(self, user_id):
        """
        Delete a user by their ID.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            bool: True if the user was deleted successfully, False otherwise.
        """
        return self.user_repository.delete_user(user_id)

    def list_users(self, params: PaginationParams) -> PaginatedResponse[UserOut]:
        """
        List paginated users.

        Args:
            params (PaginationParams): Pagination parameters.

        Returns:
            PaginatedResponse[UserOut]: The paginated list of users.
        """
        limit = params.limit
        offset = (params.page - 1) * params.limit

        total_items, users = self.user_repository.list_users(limit=limit, offset=offset)

        # Convert SQLAlchemy objects to Pydantic models
        user_list = [UserOut.model_validate(user) for user in users]

        return PaginatedResponse[UserOut](
            items=user_list,
            pagination=Paginated(
                total_items=total_items,
                total_pages=(total_items + params.limit - 1) // params.limit,
                back=params.page - 1 if params.page > 1 else None,
                next=(
                    params.page + 1
                    if params.page * params.limit < total_items
                    else None
                ),
            ),
        )

    def retrieve_user(self, user_id: str) -> UserDetail:
        """
        Retrieve a specific user by their ID.

        Args:
            user_id (str): The ID of the user.

        Returns:
            UserDetail: The details of the retrieved user.
        """
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise CustomAPIException(detail="User not found", status_code=404)
        return UserDetail.model_validate(user)
