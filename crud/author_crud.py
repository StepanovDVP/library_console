from file_manager.file_manager import json_file_authors_manager
from models.models import Author

from .base_crud import CRUDBase


class CRUDAuthor(CRUDBase):

    def get_author(self, id_: int):
        """Получить данные автора по его ID."""
        return self.data['elements'][id_]

    def get_author_name(self, id_: int):
        """Получить имя автора по его ID."""
        return self.get_author(id_)['full_name']

    def get_author_id(self, name: str) -> str | None:
        """Получить ID автора по его имени."""
        return self.data['index_by_title'].get(name)

    def add_entity(self, name: str) -> Author:
        """Добавить нового автора."""
        new_author_id = self._increment_id()
        author = self.model(id=new_author_id, full_name=name)
        self.data['elements'][new_author_id] = author.__dict__
        self.data['index_by_title'][name] = new_author_id
        self._save()
        return author

    def add_books_for_author(
            self, author_ids: list[int], book_id: int
    ) -> None:
        """
        Добавить книгу нескольким авторам.
        """
        for author_id in author_ids:
            author = self.data['elements'].get(author_id)

            if author['books'] is None:
                author['books'] = []

            if book_id not in author['books']:
                author['books'].append(book_id)

        self._save()

    def remove_books_from_authors(
            self, author_ids: list[int], book_id: int
    ) -> None:
        """
        Удалить книгу из списков у указанных авторов.
        """
        for author_id in author_ids:
            author = self.data['elements'].get(author_id)
            if author and book_id in author.get('books', []):
                author['books'].remove(book_id)

        self._save()


author_crud = CRUDAuthor(json_file_authors_manager, Author)
