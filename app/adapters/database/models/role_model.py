"""
Role model definition.
"""

from adapters.database.models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Role(BaseModel):
    """
    Role model representing a role assigned to users in the system.

    Attributes:
        name (str): The name of the role, which must be unique.
        description (str): A brief description of the role's purpose.
    """

    __tablename__ = "role"
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    users = relationship("UserRole", back_populates="role")
    permissions = relationship("RolePermission", back_populates="role")
