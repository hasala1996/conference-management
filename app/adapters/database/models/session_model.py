"""
Session-related models definition.
"""

from adapters.database.models.base_model import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship


class Session(BaseModel):
    """
    Session model representing a session in the system.

    Attributes:
        title (str): The title of the session.
        description (str): A brief description of the session.
        start_time (datetime): The starting time of the session.
        end_time (datetime): The ending time of the session.
        capacity (int): The maximum number of attendees allowed for the session.
        is_active (bool): Whether the session is active or not.
    """

    __tablename__ = "session"

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

    speakers = relationship("SpeakerAssignment", back_populates="session", cascade="all, delete-orphan")
    attendees = relationship("SessionAttendee", back_populates="session", cascade="all, delete-orphan")

