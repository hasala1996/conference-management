"""
RolePermission model definition.
"""

from adapters.database.models.base_model import BaseModel
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class RolePermission(BaseModel):
    """
    RolePermission model representing the relationship between roles and permissions.

    Attributes:
        role_id (UUID): The ID of the associated role.
        permission_id (UUID): The ID of the associated permission.
    """

    __tablename__ = "role_permission"

    role_id = Column(UUID(as_uuid=True), ForeignKey("role.id"), nullable=False)
    permission_id = Column(
        UUID(as_uuid=True), ForeignKey("permission.id"), nullable=False
    )

    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")
