from dataclasses import dataclass
from enum import StrEnum
from typing import TypeAlias

AuthorID: TypeAlias = int
BooksID: TypeAlias = int


class StatusBook(StrEnum):
    AVAILABLE = 'в наличии'
    ISSUED = 'выдана'


@dataclass
class Base:
    id: int


@dataclass
class Author(Base):
    full_name: str
    books: list[BooksID] = None


@dataclass
class Book(Base):
    title: str
    author: list[AuthorID]
    year: str
    status: StatusBook = StatusBook.AVAILABLE
