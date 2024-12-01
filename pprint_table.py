from constant import HEADLINES
from crud import author_crud


def format_authors(authors: str, max_length: int = 35) -> str:
    """
    Форматирует строку с авторами:
    """
    if len(authors) > max_length:
        authors = authors[:max_length] + ' и другие...'

    return authors


def print_books_table(data: dict) -> None:
    """
    Выводит данные о книгах в виде таблицы, включая полные имена авторов.

    :param data: Словарь с данными¬ о книгах.
    """

    print(f'{HEADLINES[0]:<5} {HEADLINES[1]:<20} {HEADLINES[2]:<50} '
          f'{HEADLINES[3]:<6} {HEADLINES[4]:<12}')
    print('-' * 94)

    for book_id, book_info in data.items():
        authors_names = [
            author_crud.get_author_name(author_id)
            for author_id in book_info['author']
        ]
        authors_str = ', '.join(authors_names)
        formatted_authors = format_authors(authors_str)

        print(
            f'{book_id:<5} {book_info['title']:<20} {formatted_authors:<50} '
            f'{book_info['year']:<6} {book_info['status']:<12}'
        )
