from constant import (
    ADD_BOOK, CHANGE_STATUS_BOOK, DELETE_BOOK, EXIT,
    SEARCH_BOOK, SHOW_BOOKS
)
from crud import author_crud, book_crud
from models.models import StatusBook
from pprint_table import print_books_table
from router import Router
from services import LibraryService
from utils import get_choice_input, get_int_input
from validators import check_name, get_or_create_author, validate_year

router = Router()


@router.filter(lambda cmd: cmd == ADD_BOOK[0])
def add_book():
    """Добавить новую книгу."""
    title_book = input('Введите название книги: ')

    authors = set()
    while True:
        author_name = input('Введите имя автора книги: ')

        check_name(author_name)

        author_id = get_or_create_author(author_name)
        authors.add(author_id)

        cont = get_choice_input(
            'Добавить автора? (Y/N) ', ['Y', 'N']
        )
        if cont == 'N':
            break

    year_book = input('Укажите год издания книги: ')
    validate_year(year_book)

    new_book = LibraryService.add_book_with_authors(
        title=title_book,
        authors=list(authors),
        year=year_book
    )

    print(f'Книга "{new_book.title}" успешно добавлена с ID: {new_book.id}')


@router.filter(lambda cmd: cmd == DELETE_BOOK[0])
def delete_book():
    """Удалить книгу по ID."""
    id_book = get_int_input('Введите ID книги: ')

    book = book_crud.get_book_by_id(id_book)
    if not book:
        raise LookupError(f'Книга с ID {id_book} не найдена!')

    LibraryService.delete_book_and_update_authors(book)
    print(f'Книга с ID {id_book} успешно удалена!')


@router.filter(lambda cmd: cmd == SEARCH_BOOK[0])
def search_book():
    """Поиск книги по автору, названию или году издания."""
    book_found = None
    param = get_choice_input(
        '1 - Наименование книги\n'
        '2 - Автор книги\n'
        '3 - Год издания\n'
        'Укажите параметр поиска: ',
        ['1', '2', '3'], 'Неверный выбор.'
    )

    if param == "1":
        title = input("Введите название книги: ")
        book_found = book_crud.search_book_by_title(title)

    elif param == "2":
        author_name = input("Введите имя автора: ")
        author_id = author_crud.get_author_id(author_name)

        if author_id:
            author_data = author_crud.get_author(author_id)
            book_found = book_crud.get_books_by_ids(author_data['books'])

    elif param == "3":
        year = validate_year(input("Введите год издания книги: "))
        if year:
            book_found = book_crud.search_book_by_year(year)

    if not book_found:
        raise LookupError('Книга не найдена!')

    print_books_table(book_found)


@router.filter(lambda cmd: cmd == SHOW_BOOKS[0])
def show_books():
    """Показать все книги."""
    data = book_crud.get_all_books()
    print_books_table(data)


@router.filter(lambda cmd: cmd == CHANGE_STATUS_BOOK[0])
def change_status_book():
    """Изменить статус книги."""
    id_book = get_int_input('Введите ID книги: ')

    book = book_crud.get_book_by_id(id_book)
    if not book:
        print(f'Книга с ID {id_book} не найдена!')
        return

    print(f'Текущий статус книги "{book['title']}" '
          f'(ID: {id_book}): {book['status']}')

    new_status = get_choice_input(
        'Выберите новый статус книги:\n'
        '1 - В наличии\n'
        '2 - Выдана\n'
        'Введите номер статуса: ',
        ['1', '2'], 'Неверный выбор.'
    )
    status = StatusBook.AVAILABLE

    if new_status == '2':
        status = StatusBook.ISSUED

    book_crud.update_book_status(book, status)

    print(f'Статус книги с ID {id_book} успешно изменен на "{status.value}"!')
    return


@router.filter(lambda cmd: cmd == EXIT[0])
def exit_program():
    print('Выход из приложения.')
    exit(0)
