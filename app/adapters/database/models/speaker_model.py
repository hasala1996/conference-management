"""
Session-related models definition.
"""

from adapters.database.models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship



class Speaker(BaseModel):
    """
    Speaker model representing a speaker who can be assigned to sessions.

    Attributes:
        name (str): The name of the speaker.
        email (str): The email address of the speaker.
        biography (str): A brief biography of the speaker.
    """

    __tablename__ = "speaker"

    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    biography = Column(String, nullable=True)

    assignments = relationship("SpeakerAssignment", back_populates="speaker", cascade="all, delete-orphan")


