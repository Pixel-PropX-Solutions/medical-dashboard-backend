from typing import TypeVar, Generic, Sequence
from pydantic import BaseModel, ConfigDict
from math import ceil

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: Sequence[T]
    total: int
    page: int
    size: int
    pages: int
    
    model_config = ConfigDict(from_attributes=True)

def paginate(items: Sequence[T], total: int, page: int, size: int) -> PaginatedResponse[T]:
    pages = ceil(total / size) if size > 0 else 0
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=pages
    )
