"""
Verify permission dependency.
"""

from typing import Callable

from adapters.api.dependencies import get_db
from adapters.database.models import Permission, RolePermission, User
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from .authorizer import get_user_authorizer


def verify_permission(permission_codename: str) -> Callable:
    """
    Dependency function to verify if the authenticated user has the required permission.

    Args:
        permission_codename (str): The codename of the permission to verify.

    Returns:
        Callable: A dependency function to be used in routes.

    Raises:
        HTTPException: If the user does not have the required permission.
    """

    async def _verify_permission(
        data_base: Session = Depends(get_db),
        user: User = Depends(get_user_authorizer),
    ) -> None:
        """
        Inner function to perform the permission check.

        Args:
            request (Request): The incoming request.
            data_base (Session): The database session.
            user (User): The authenticated user.

        Raises:
            HTTPException: If the user does not have the required permission.
        """
        # Check if the user has the required permission
        has_permission = (
            data_base.query(RolePermission)
            .join(RolePermission.role)
            .join(RolePermission.permission)
            .filter(
                RolePermission.role_id.in_([role.role_id for role in user.roles]),
                Permission.name == permission_codename,  # Required permission
            )
            .exists()
        )

        if not data_base.query(has_permission).scalar():
            raise HTTPException(
                status_code=403,
                detail="User does not have the required permission.",
            )

    return _verify_permission
