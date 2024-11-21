"""
UserRole model definition.
"""

from adapters.database.models.base_model import BaseModel
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class UserRole(BaseModel):
    """
    UserRole model representing the relationship between users and roles.

    Attributes:
        user_id (UUID): The ID of the associated user.
        role_id (UUID): The ID of the associated role.
        assigned_at (datetime): The date and time when the role was assigned to the user.
    """

    __tablename__ = "user_role"

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("role.id"), nullable=False)

    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="user")
