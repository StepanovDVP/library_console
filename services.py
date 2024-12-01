from crud import author_crud, book_crud
from models.models import Book


class LibraryService:
    """
    Сервис для управления книгами и авторами.
    """

    @staticmethod
    def add_book_with_authors(
            title: str, authors: list[int], year: str
    ) -> Book:
        """
        Добавить книгу и обновить соответствующих авторов.
        """
        new_book = book_crud.add_entity(
            title=title, authors=authors, year=year
        )
        author_crud.add_books_for_author(authors, new_book.id)

        return new_book

    @staticmethod
    def delete_book_and_update_authors(book: dict) -> None:
        """
        Удалить книгу и обновить списки книг у авторов.
        """
        book_crud.delete_book(book['id'])
        author_crud.remove_books_from_authors(book['author'], book['id'])
