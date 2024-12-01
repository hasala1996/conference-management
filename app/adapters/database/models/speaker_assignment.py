"""
Session-related models definition.
"""

from adapters.database.models.base_model import BaseModel
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class SpeakerAssignment(BaseModel):
    """
    SpeakerAssignment model representing the assignment of a speaker to a session.

    Attributes:
        session_id (int): The ID of the session.
        speaker_id (int): The ID of the speaker.
        role (str): The role of the speaker in the session (e.g., presenter, panelist).
    """

    __tablename__ = "speaker_assignment"

    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("scheduled_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    speaker_id = Column(
        UUID(as_uuid=True), ForeignKey("speaker.id", ondelete="CASCADE"), nullable=False
    )
    role = Column(String, nullable=False)

    session = relationship("ScheduledSession", back_populates="speakers")
    speaker = relationship("Speaker", back_populates="assignments")
