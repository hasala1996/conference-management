"""
Authentication service.
"""

from datetime import datetime, timedelta

import jwt
from config import settings
from core.auth.ports.repository import UserRepository
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """
    Service for authentication and token management.
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def authenticate_user(self, email: str, password: str):
        """
        Authenticate a user by email and password.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            User: The authenticated user object or None if authentication fails.
        """
        user = self.user_repository.get_by_email(email)
        if not user or not self.verify_password(password, user.password):
            return None
        return user

    def create_access_token(self, data: dict):
        """
        Create a JWT access token.

        Args:
            data (dict): Data to include in the token.

        Returns:
            str: The JWT token.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.

        Args:
            plain_password (str): The plain text password.
            hashed_password (str): The hashed password.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return pwd_context.verify(plain_password, hashed_password)
