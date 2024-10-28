from typing import List, TypeVar, Generic
from pydantic import BaseModel
from .constants import PAGE_SIZE


T = TypeVar('T', bound=BaseModel)

class PaginationSchema(BaseModel, Generic[T]):
    total: int
    page: int
    total_pages: int
    items: List[T]


def paginate(page: int, total: int, items: List[T]) -> PaginationSchema[T]:
    return {
        "total": total,
        "page": page,
        "total_pages": (total // PAGE_SIZE) + 1 if total % PAGE_SIZE else total // PAGE_SIZE,
        "items": items
    }