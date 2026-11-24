from typing import Any, Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Any = None

class MetaPagination(BaseModel):
    total: int
    page: int = 1
    page_size: int = 20

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    meta: Optional[Any] = None
    error: Optional[ErrorDetail] = None

    @classmethod
    def ok(cls, data: T, meta: Optional[Any] = None) -> "ApiResponse[T]":
        return cls(success=True, data=data, meta=meta, error=None)

    @classmethod
    def fail(cls, code: str, message: str, details: Any = None) -> "ApiResponse[None]":
        return cls(
            success=False,
            data=None,
            meta=None,
            error=ErrorDetail(code=code, message=message, details=details),
        )
