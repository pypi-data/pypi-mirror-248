from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class CursorPaginatedResource(Generic[T]):
    next: str
    previous: str
    results: list[T]


@dataclass
class PagePaginatedResource(Generic[T]):
    count: int
    next: str
    previous: str
    results: list[T]
