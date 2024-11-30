from typing import Generic, List, Optional, TypeVar

from fastapi import Query
from pydantic import BaseModel

T = TypeVar("T")


class PaginationParams(BaseModel):
    """
    Pagination parameters for the API.
    """

    page: int = Query(1, ge=1, description="Page number (1-based index)")
    limit: int = Query(10, ge=1, le=100, description="Items per page")
    search: Optional[str] = Query(None, max_length=100, description="Search term")


class Paginated(BaseModel):
    """
    Pagination metadata for API responses.
    """

    total_items: int
    total_pages: int
    back: Optional[int]
    next: Optional[int]


class PaginatedResponse(BaseModel, Generic[T]):
    """
    A paginated API response.
    """

    items: List[T]
    pagination: Paginated
