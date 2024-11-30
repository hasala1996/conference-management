from typing import List

from core.auth.schemas import UserCreate, UserDetail, UserOut, UserUpdate
from core.auth.user_service import UserService
from core.common.pagination import PaginatedResponse, PaginationParams
from dependencies.user_repository import get_user_service
from dependencies.verify_permission import verify_permission
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[UserOut],
    dependencies=[Depends(verify_permission("manage_users"))],
)
def list_users(
    service: UserService = Depends(get_user_service),
    pagination: PaginationParams = Depends(),
) -> PaginatedResponse[UserOut]:
    """
    Retrieve a list of all users.

    Args:
        service (UserService): The user service instance.

    Returns:
        List[User]: A list of all users.
    """
    return service.list_users(params=pagination)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut,
    dependencies=[Depends(verify_permission("manage_users"))],
)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    """
    Create a new user.

    Args:
        user (UserCreate): The data required to create a new user.
        service (UserService): The user service instance.

    Returns:
        dict: A dictionary with the created user's email and ID.
    """
    created_user = service.create_user(user)
    return created_user


@router.put(
    "/{user_id}",
    response_model=UserUpdate,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_permission("manage_users"))],
)
def update_user(
    user_id: str,
    user: UserUpdate,
    service: UserService = Depends(get_user_service),
):
    """
    Update an existing user by their ID.

    Args:
        user_id (str): The ID of the user to update.
        user (UserUpdate): The updated user data.
        service (UserService): The user service instance.

    Returns:
        dict: A dictionary with the updated user's email and ID.
    """
    updated_user = service.update_user(user_id, user)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "id": str(updated_user.id),
            "email": updated_user.email,
            "is_active": updated_user.is_active,
        },
    )


@router.delete("/{user_id}", dependencies=[Depends(verify_permission("manage_users"))])
def delete_user(user_id: str, service: UserService = Depends(get_user_service)):
    """
    Delete a user by their ID.

    Args:
        user_id (str): The ID of the user to delete.
        service (UserService): The user service instance.

    Returns:
        dict: A message confirming the deletion of the user.
    """
    service.delete_user(user_id)
    return {"message": "User deleted successfully"}


@router.get(
    "/{user_id}",
    response_model=UserDetail,
    dependencies=[Depends(verify_permission("manage_users"))],
    status_code=status.HTTP_200_OK,
)
def retrieve_user(
    user_id: str, service: UserService = Depends(get_user_service)
) -> UserDetail:
    """
    Retrieve a specific user by their ID.

    Args:
        user_id (str): The ID of the user to retrieve.
        service (UserService): The user service instance.

    Returns:
        UserDetail: The retrieved user's details.
    """
    return service.retrieve_user(user_id)
