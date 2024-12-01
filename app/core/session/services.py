from core.common.pagination import Paginated, PaginatedResponse, PaginationParams
from core.session.ports.session_repository import SessionRepository
from core.session.schemas import (
    SessionCreate,
    SessionDetail,
    SessionListOut,
    SessionOut,
    SessionUpdate,
    SpeakerOut,
)


class SessionService:
    def __init__(self, session_repository: SessionRepository):
        """Initialize the session service with a session repository.

        Args:
            session_repository (SessionRepository): The session repository.
        """
        self.session_repository = session_repository

    def create_session(self, session_data: SessionCreate) -> SessionOut:
        """Create a new session and assign speakers if provided.

        Args:
            session_data (SessionCreate): The data to create the session.

        Returns:
            SessionOut: The created session.
        """
        new_session = self.session_repository.create_session(session_data)

        if session_data.speakers:
            for speaker_id in session_data.speakers:
                speaker = self.session_repository.get_speaker_by_id(speaker_id)
                if not speaker:
                    raise ValueError(f"Speaker with ID {speaker_id} does not exist.")
                self.session_repository.assign_speaker_to_session(
                    new_session.id, speaker_id
                )

        return new_session

    def get_session(self, session_id: str) -> SessionDetail:
        """Get session details by its ID.

        Args:
            session_id (str): The ID of the session.

        Returns:
            SessionDetail: The session details.
        """
        session = self.session_repository.get_session_by_id(session_id)
        if not session:
            raise ValueError(f"Session with ID {session_id} not found.")
        return session

    def update_session(
        self, session_id: str, session_data: SessionUpdate
    ) -> SessionOut:
        """Update an existing session with new data.

        Args:
            session_id (str): The ID of the session to update.
            session_data (SessionUpdate): The new data for the session.

        Returns:
            SessionOut: The updated session.
        """
        # Exclude unset fields to avoid overwriting with None
        update_data = session_data.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No valid fields provided for update.")
        return self.session_repository.update_session(session_id, update_data)

    def delete_session(self, session_id: str) -> None:
        """Delete a session by its ID.

        Args:
            session_id (str): The ID of the session to delete.
        """
        self.session_repository.delete_session(session_id)

    def list_sessions(
        self, params: PaginationParams
    ) -> PaginatedResponse[SessionListOut]:
        """List sessions with pagination.

        Args:
            params (PaginationParams): The pagination parameters.

        Returns:
            PaginatedResponse[SessionListOut]: The paginated response of sessions.
        """
        limit = params.limit
        offset = (params.page - 1) * params.limit

        total_items, sessions = self.session_repository.list_sessions(
            limit=limit, offset=offset
        )

        session_list = [SessionListOut.model_validate(session) for session in sessions]

        return PaginatedResponse[SessionListOut](
            items=session_list,
            pagination=Paginated(
                total_items=total_items,
                total_pages=(total_items + params.limit - 1) // params.limit,
                back=params.page - 1 if params.page > 1 else None,
                next=(
                    params.page + 1
                    if params.page * params.limit < total_items
                    else None
                ),
            ),
        )

    def list_speakers(self, params: PaginationParams) -> PaginatedResponse[SpeakerOut]:
        """List speakers with pagination.

        Args:
            params (PaginationParams): The pagination parameters.

        Returns:
            PaginatedResponse[SpeakerOut]: The paginated response of speakers.
        """
        limit = params.limit
        offset = (params.page - 1) * params.limit

        total_items, speakers = self.session_repository.list_speakers(
            limit=limit, offset=offset
        )

        speaker_list = [
            SpeakerOut(
                id=str(speaker.id),
                name=speaker.name,
                email=speaker.email,
                biography=speaker.biography,
            )
            for speaker in speakers
        ]

        return PaginatedResponse[SpeakerOut](
            items=speaker_list,
            pagination=Paginated(
                total_items=total_items,
                total_pages=(total_items + params.limit - 1) // params.limit,
                back=params.page - 1 if params.page > 1 else None,
                next=(
                    params.page + 1
                    if params.page * params.limit < total_items
                    else None
                ),
            ),
        )
