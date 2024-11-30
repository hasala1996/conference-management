"""
This module contains the authorizer function to validate the JWT token.
"""

from typing import Optional

import jwt
from adapters.database.models import User
from config import settings
from core.auth.ports.repository import UserRepository
from dependencies.user_repository import get_user_repository
from fastapi import Depends, HTTPException, Request
from fastapi.datastructures import FormData


async def get_user_authorizer(
    request: Request,
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    """
    Retrieves the user from the request's authorization token.
    The token must be in the format: Bearer <token>, where <token> is the JWT token.
    Otherwise, it will raise an HTTPException with status code 401.

    Args:
        request (Request): The incoming request object.

    Returns:
        User: The authenticated user.

    Raises:
        HTTPException: If the token is expired or invalid, or if the user does not exist.
    """
    auth_header: str = request.headers.get("Authorization", "")
    token: Optional[str] = None

    if auth_header:
        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=401, detail="Invalid token format. Bearer token required."
            )
        token = auth_header.split(" ")[1]
    else:
        if request.method in ["POST"]:
            form_data: FormData = await request.form()
            token = form_data.get("authorization_token")
    if not token:
        raise HTTPException(status_code=401, detail="Authorization token missing")

    try:
        token_decode: dict[str, str] = jwt.decode(
            jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"]
        )
        user: Optional[User] = user_repository.get_user_by_id(
            user_id=token_decode.get("user_id", "")
        )
        if not user:
            raise HTTPException(status_code=404, detail="User does not exist")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token expired or invalid. Try again, please.",
        )
