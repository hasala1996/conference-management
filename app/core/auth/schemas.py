"""
Schemas for authentication and login.
"""

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
