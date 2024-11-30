"""
Session-related models definition.
"""

from adapters.database.models.base_model import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func



class SessionAttendee(BaseModel):
    """
    SessionAttendee model representing an attendee in a session.

    Attributes:
        session_id (int): The ID of the session.
        user_id (int): The ID of the user attending the session.
        attendance_time (datetime): The time the user attended the session.
    """

    __tablename__ = "session_attendee"

    session_id = Column(ForeignKey("session.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    attendance_time = Column(DateTime, default=func.now())

    session = relationship("Session", back_populates="attendees")
    user = relationship("User")
