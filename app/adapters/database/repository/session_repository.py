from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from adapters.database.models import ScheduledSession, Speaker, SpeakerAssignment
from core.session.ports.session_repository import SessionRepository
from core.session.schemas import (
    SessionCreate,
    SessionDetail,
    SessionListOut,
    SessionOut,
    SessionUpdate,
    SpeakerOut,
)
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, joinedload


class SessionRepositoryImpl(SessionRepository):
    def __init__(self, db_session: Session):
        """Initialize the session repository with a database session."""
        self.db_session = db_session

    def create_session(self, session_data: SessionCreate) -> SessionOut:
        """Create a new session with the provided session data.

        Args:
            session_data (SessionCreate): The data required to create a new session.

        Returns:
            SessionOut: The created session.
        """
        new_session = ScheduledSession(**session_data.model_dump(exclude={"speakers"}))
        self.db_session.add(new_session)
        self.db_session.commit()
        self.db_session.refresh(new_session)
        return SessionOut.model_validate(new_session)

    def get_session_by_id(self, session_id: UUID) -> Optional[SessionDetail]:
        """Retrieve a session by its UUID, including its speakers."""
        try:
            session = (
                self.db_session.query(ScheduledSession)
                .options(
                    joinedload(ScheduledSession.speakers).joinedload(
                        SpeakerAssignment.speaker
                    )
                )
                .filter(
                    ScheduledSession.id == session_id,
                    ScheduledSession.deleted_at.is_(None),
                )
                .one()
            )

            speakers = [
                SpeakerOut(
                    id=str(assignment.speaker.id),
                    name=assignment.speaker.name,
                    email=assignment.speaker.email,
                    role=assignment.role,
                    biography=assignment.speaker.biography,
                )
                for assignment in session.speakers
            ]
            session_dict = session.__dict__.copy()
            session_dict.pop("speakers", None)
            session_data = SessionDetail.model_validate(session_dict)
            session_data.speakers = speakers

            return session_data
        except NoResultFound:
            return None

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
        session = (
            self.db_session.query(ScheduledSession)
            .filter(
                ScheduledSession.id == session_id, ScheduledSession.deleted_at.is_(None)
            )
            .one_or_none()
        )

        if not session:
            raise NoResultFound("Session not found")

        for key, value in session_data.items():
            setattr(session, key, value)

        self.db_session.commit()
        self.db_session.refresh(session)
        return SessionOut.model_validate(session)

    def delete_session(self, session_id: UUID) -> None:
        """Delete a session by its UUID.

        Args:
            session_id (UUID): The UUID of the session to delete.
        """
        session = (
            self.db_session.query(ScheduledSession)
            .filter(
                ScheduledSession.id == session_id, ScheduledSession.deleted_at.is_(None)
            )
            .one_or_none()
        )

        if not session:
            raise NoResultFound("Session not found")

        session.deleted_at = datetime.now(timezone.utc)
        self.db_session.commit()

    def list_sessions(
        self, limit: int, offset: int
    ) -> tuple[int, list[SessionListOut]]:
        """List sessions with pagination.

        Args:
            limit (int): The maximum number of sessions to return.
            offset (int): The number of sessions to skip before starting to collect the result set.

        Returns:
            tuple[int, list[SessionListOut]]: A tuple containing the total number of sessions and a list of sessions.
        """
        query = self.db_session.query(ScheduledSession).filter(
            ScheduledSession.deleted_at.is_(None)
        )
        total = query.count()
        sessions = query.offset(offset).limit(limit).all()
        return total, [session.__dict__.copy() for session in sessions]

    def assign_speaker_to_session(self, session_id: UUID, speaker_id: UUID) -> None:
        """Assign a speaker to a session.

        Args:
            session_id (UUID): The UUID of the session to assign the speaker to.
            speaker_id (UUID): The UUID of the speaker to assign to the session.
        """
        speaker_assignment = SpeakerAssignment(
            session_id=str(session_id),
            speaker_id=str(speaker_id),
            role="Presenter",
        )

        self.db_session.add(speaker_assignment)
        self.db_session.commit()

    def list_speakers(self, limit: int, offset: int) -> tuple[int, list[SpeakerOut]]:
        """
        List speakers with pagination.

        Args:
            limit (int): The maximum number of speakers to return.
            offset (int): The number of speakers to skip before starting to collect the result set.

        Returns:
            Tuple[int, List[SpeakerOut]]: A tuple containing the total number of speakers and a list of speakers.
        """
        query = self.db_session.query(Speaker)
        total = query.count()
        speakers = query.offset(offset).limit(limit).all()
        return total, speakers

    def get_speaker_by_id(self, speaker_id: UUID) -> Optional[SpeakerOut]:
        """
        Retrieve a speaker by its ID.
        """
        speaker = (
            self.db_session.query(Speaker)
            .filter(Speaker.id == speaker_id)
            .one_or_none()
        )
        if speaker:
            return SpeakerOut.model_validate(
                {
                    "id": str(speaker.id),
                    "name": speaker.name,
                    "email": speaker.email,
                    "biography": speaker.biography,
                }
            )

        return None
