from file_manager.file_manager import json_file_books_manager
from models.models import Book

from .base_crud import CRUDBase


class CRUDBook(CRUDBase):

    def get_all_books(self):
        """Вернуть все книги."""
        return self.data['elements']

    def get_book_by_id(self, id_: int) -> dict | None:
        """Получить книгу по ID."""
        return self.data['elements'].get(id_)

    def get_books_by_ids(self, ids: list) -> dict:
        """Получить словарь книг по их ID."""
        return {book_id: self.get_book_by_id(book_id) for book_id in ids}

    def search_book_by_year(self, year: str):
        """Поиск книги по году издания."""
        book_ids = self.data['index_by_year'].get(year, [])
        books_found = self.get_books_by_ids(book_ids)
        return books_found if books_found else None

    def search_book_by_title(self, title: str) -> dict | None:
        """Поиск книги по наименованию."""
        book_ids = self.data['index_by_title'].get(title, [])
        books_found = self.get_books_by_ids(book_ids)
        return books_found if books_found else None

    def add_entity(self, title: str, authors: list[int], year: str) -> Book:
        """Добавить новую книгу."""
        new_book_id = self._increment_id()
        book = self.model(
            id=new_book_id, title=title, author=authors, year=year
        )

        self.data['elements'][new_book_id] = book.__dict__
        self.data['index_by_title'].setdefault(title, []).append(new_book_id)
        self.data['index_by_year'].setdefault(year, []).append(new_book_id)

        self._save()

        return book

    def delete_book(self, id_: int) -> None:
        """Удалить книгу."""

        book = self.data['elements'].pop(id_)

        title = book['title']
        self.data['index_by_title'][title].remove(id_)
        if not self.data['index_by_title'][title]:
            del self.data['index_by_title'][title]

        year = book['year']

        self.data['index_by_year'][year].remove(id_)
        if not self.data['index_by_year'][year]:
            del self.data['index_by_year'][year]

        self._save()

    def update_book_status(self, book: dict, new_status: str) -> None:
        """Обновить статус книги, передав саму книгу и новый статус."""
        book['status'] = new_status
        self._save()


book_crud = CRUDBook(json_file_books_manager, Book)
