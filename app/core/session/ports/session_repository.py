"""
Session repository interface.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from uuid import UUID

from core.session.schemas import (
    SessionCreate,
    SessionDetail,
    SessionOut,
    SessionUpdate,
    SpeakerOut,
)


class SessionRepository(ABC):
    """Session repository interface."""

    @abstractmethod
    def create_session(self, session_data: SessionCreate) -> SessionOut:
        """Create a new session with the provided session data.

        Args:
            session_data (SessionCreate): The data required to create a new session.

        Returns:
            SessionOut: The created session.
        """

    @abstractmethod
    def get_session_by_id(self, session_id: UUID) -> Optional[SessionDetail]:
        """Retrieve a session by its UUID.

        Args:
            session_id (UUID): The UUID of the session to retrieve.

        Returns:
            Optional[SessionOut]: The session with the specified UUID, or None if not found.
        """

    @abstractmethod
    def update_session(
        self, session_id: UUID, session_data: SessionUpdate
    ) -> SessionOut:
        """Update an existing session with new data.

        Args:
            session_id (UUID): The UUID of the session to update.
            session_data (SessionUpdate): The new data for the session.

        Returns:
            SessionOut: The updated session.
        """

    @abstractmethod
    def delete_session(self, session_id: UUID) -> None:
        """Delete a session by its UUID.

        Args:
            session_id (UUID): The UUID of the session to delete.
        """

    @abstractmethod
    def list_sessions(self, limit: int, offset: int) -> Tuple[int, List[SessionOut]]:
        """List sessions with pagination.

        Args:
            limit (int): The maximum number of sessions to return.
            offset (int): The number of sessions to skip before starting to collect the result set.

        Returns:
            Tuple[int, List[SessionOut]]: A tuple containing the total number of sessions and a list of sessions.
        """

    @abstractmethod
    def assign_speaker_to_session(self, session_id: UUID, speaker_id: UUID) -> None:
        """
        Assign a speaker to a session.
        """

    @abstractmethod
    def list_speakers(self, limit: int, offset: int) -> tuple[int, list[SpeakerOut]]:
        """
        List speakers with pagination.

        Args:
            limit (int): The maximum number of speakers to return.
            offset (int): The number of speakers to skip before starting to collect the result set.

        Returns:
            Tuple[int, List[SpeakerOut]]: A tuple containing the total number of speakers and a list of speakers.
        """

    @abstractmethod
    def get_speaker_by_id(self, speaker_id: UUID) -> Optional[SpeakerOut]:
        """
        Retrieve a speaker by its ID.
        """
