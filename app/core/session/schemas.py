from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    """
    Schema for detailed session information, including speakers.
    """

    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    capacity: int
    speakers: Optional[List[UUID]] = None

    class Config:
        from_attributes = True


class SessionUpdate(BaseModel):
    """
    Schema for updating an existing session.
    """

    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    start_time: Optional[datetime] = Field(default=None)
    end_time: Optional[datetime] = Field(default=None)
    capacity: Optional[int] = Field(default=None)


class SpeakerOut(BaseModel):
    """
    Schema for outputting speaker information.
    """

    id: str
    name: str
    email: str
    role: Optional[str] = None
    biography: Optional[str] = None

    class Config:
        from_attributes = True


class SessionOut(BaseModel):
    """
    Schema for outputting session information.
    """

    id: UUID
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    capacity: int
    is_active: bool

    class Config:
        from_attributes = True


class SessionDetail(BaseModel):
    """
    Schema for detailed session information, including speakers.
    """

    id: UUID
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    capacity: int
    is_active: bool
    speakers: Optional[List[SpeakerOut]] = None

    class Config:
        from_attributes = True


class SessionListOut(BaseModel):
    """
    Schema for outputting a list of sessions.
    """

    id: UUID
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    capacity: int
    is_active: bool

    class Config:
        from_attributes = True
