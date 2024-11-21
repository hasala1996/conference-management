"""
User model definition.
"""

from adapters.database.models.base_model import BaseModel
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship


class User(BaseModel):
    """
    User model representing a user in the system.

    Attributes:
        email (str): The user's email address, which must be unique.
        password (str): The hashed password for the user.
        is_active (bool): Whether the user is active in the system.
    """

    __tablename__ = "user"

    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    roles = relationship("UserRole", back_populates="user")
