"""
Session API endpoints.
"""

from core.common.pagination import PaginatedResponse, PaginationParams
from core.session.schemas import (
    SessionCreate,
    SessionDetail,
    SessionListOut,
    SessionOut,
    SessionUpdate,
    SpeakerOut,
)
from core.session.services import SessionService
from dependencies.session_service import get_session_service
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.get("/speakers", response_model=PaginatedResponse[SpeakerOut])
def list_speakers(
    session_service: SessionService = Depends(get_session_service),
    pagination: PaginationParams = Depends(),
):
    """
    List all speakers with pagination.

    Args:
        session_service (SessionService): The session service dependency.
        pagination (PaginationParams): Pagination parameters.

    Returns:
        PaginatedResponse[SpeakerOut]: A paginated list of speakers.
    """
    return session_service.list_speakers(params=pagination)


@router.post("/", response_model=SessionOut, status_code=status.HTTP_201_CREATED)
def create_session(
    session_data: SessionCreate,
    session_service: SessionService = Depends(get_session_service),
):
    """
    Create a new session.

    Args:
        session_data (SessionCreate): The data required to create a session.
        session_service (SessionService): The session service dependency.

    Returns:
        SessionOut: The created session.
    """
    return session_service.create_session(session_data)


@router.get("/{session_id}", response_model=SessionDetail)
def get_session(
    session_id: str, session_service: SessionService = Depends(get_session_service)
):
    """
    Retrieve a session by its ID.

    Args:
        session_id (str): The ID of the session to retrieve.
        session_service (SessionService): The session service dependency.

    Raises:
        HTTPException: If the session is not found.

    Returns:
        SessionDetail: The details of the session.
    """
    session = session_service.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )
    return session


@router.put("/{session_id}", response_model=SessionOut)
def update_session(
    session_id: str,
    session_data: SessionUpdate,
    session_service: SessionService = Depends(get_session_service),
):
    """
    Update an existing session.

    Args:
        session_id (str): The ID of the session to update.
        session_data (SessionUpdate): The data to update the session with.
        session_service (SessionService): The session service dependency.

    Returns:
        SessionOut: The updated session.
    """
    return session_service.update_session(session_id, session_data)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: str, session_service: SessionService = Depends(get_session_service)
):
    """
    Delete a session by its ID.

    Args:
        session_id (str): The ID of the session to delete.
        session_service (SessionService): The session service dependency.
    """
    session_service.delete_session(session_id)


@router.get("/", response_model=PaginatedResponse[SessionListOut])
def list_sessions(
    session_service: SessionService = Depends(get_session_service),
    pagination: PaginationParams = Depends(),
):
    """
    List all sessions with pagination.

    Args:
        session_service (SessionService): The session service dependency.
        pagination (PaginationParams): Pagination parameters.

    Returns:
        PaginatedResponse[SessionListOut]: A paginated list of sessions.
    """
    return session_service.list_sessions(params=pagination)
