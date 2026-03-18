"""
Standardised API response envelope (optional).
 
Use these when you want a consistent response shape:
    {
        "success": true,
        "data": { ... },
        "meta": { "page": 1, "total": 42 }
    }
"""

from typing import Any, Generic, Optional, TypeVar
 
from pydantic import BaseModel

T = TypeVar("T")


class Meta(BaseModel):
    page: int
    size: int
    total: int
    pages: int


class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None
    
class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    data: list[T]
    meta: Meta

def ok(data: Any = None, message: str | None = None) -> dict:
    return {"success": True, "data": data, "message": message}


def paginate(items: list, total: int, page: int, size: int) -> dict:
    pages = (total + size - 1) // size
    return {
        "success": True,
        "data": items,
        "meta": {"page": page, "size": size, "total": total, "pages": pages},
    }