"""
Auth endpoints.
"""

from dependencies.auth_service import get_auth_service
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.auth.schemas import LoginRequest, LoginResponse
from app.core.auth.services import AuthService

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(
    login_request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)
):
    """
    Login endpoint for user authentication.

    Args:
        login_request (LoginRequest): The login request data.
        auth_service (AuthService): The authentication service.

    Returns:
        LoginResponse: The JWT token and its type.
    """
    user = auth_service.authenticate_user(
        email=login_request.email, password=login_request.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = auth_service.create_access_token(data={"sub": user.email})
    return LoginResponse(access_token=access_token)
