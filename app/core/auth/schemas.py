"""
Schemas for authentication and login.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """
    Schema for the login request.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """

    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """
    Schema for the login response.

    Attributes:
        access_token (str): The generated JWT token.
        token_type (str): The type of the token, defaults to 'Bearer'.
    """

    access_token: str


class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        email (EmailStr): The email address of the user.
        password (str): The password for the user.
        is_active (bool): The status indicating if the user is active, defaults to True.
    """

    email: EmailStr
    password: str
    is_active: bool = True


class UserUpdate(BaseModel):
    """
    Schema for updating an existing user.

    Attributes:
        email (Optional[EmailStr]): The new email address of the user, if any.
        password (Optional[str]): The new password for the user, if any.
        is_active (Optional[bool]): The new status indicating if the user is active, if any.
    """

    email: Optional[EmailStr]
    password: Optional[str]
    is_active: Optional[bool]


class UserOut(BaseModel):
    """
    Schema for outputting user information.

    Attributes:
        id (UUID): The unique identifier of the user.
        email (EmailStr): The email address of the user.
        is_active (bool): The status indicating if the user is active.
    """

    id: UUID
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True


class UserDetail(BaseModel):
    """
    Schema for user details.

    Attributes:
        id (UUID): The unique identifier of the user.
        email (EmailStr): The email address of the user.
        is_active (bool): The status indicating if the user is active.
        created_at (datetime): The date and time the user was created.
        updated_at (datetime): The date and time the user was last updated.
    """

    id: UUID
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
