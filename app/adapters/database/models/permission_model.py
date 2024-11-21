"""
Permission model definition.
"""

from adapters.database.models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Permission(BaseModel):
    """
    Permission model representing an action that can be assigned to a role.

    Attributes:
        name (str): The unique name of the permission.
        description (str): A brief description of the permission's purpose.
    """

    __tablename__ = "permission"

    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    # Many-to-Many relationship with roles
    roles = relationship("RolePermission", back_populates="permission")
