import os

if 'tests' in os.path.abspath(os.path.curdir):
    FILE_PATH_AUTHORS = '../infra/test_authors.json'
    FILE_PATH_BOOKS = '../infra/test_books.json'
else:
    FILE_PATH_AUTHORS = 'infra/authors.json'
    FILE_PATH_BOOKS = 'infra/books.json'

ADD_BOOK = '1', 'Добавить книгу'
DELETE_BOOK = '2', 'Удалить книгу'
SEARCH_BOOK = '3', 'Найти книгу'
SHOW_BOOKS = '4', 'Показать все книги'
CHANGE_STATUS_BOOK = '5', 'Изменить статус книги'
EXIT = '6', 'Выход'

LST_COMMANDS = [
    ADD_BOOK, DELETE_BOOK,
    SEARCH_BOOK, SHOW_BOOKS,
    CHANGE_STATUS_BOOK, EXIT
]

HEADLINES = ['ID', 'Title', 'Authors', 'Year', 'Status']

APOSTOL_BOOK = 1564
