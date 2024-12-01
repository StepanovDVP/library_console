from datetime import datetime

from constant import APOSTOL_BOOK
from crud import author_crud


def check_name(name: str) -> bool:
    """Проверить корректность имя Автора."""
    if not name:
        return False

    if len(name) > 100:
        return False

    parts = name.split()

    # return all(part.isalpha() for part in parts)
    if not all(part.isalpha() for part in parts):
        raise ValueError('Имя автора введёно некорректно!')


def validate_year(year: str) -> str | None:
    """Проверить год издания книги."""
    if not year.isdigit():
        raise ValueError('Год издания книги введён некорректно!')

    year = int(year)
    current_year = datetime.now().year

    if year < APOSTOL_BOOK or year > current_year:
        raise ValueError(
            'Это должно быть положительное число, '
            'не превышающее текущий год.')

    return str(year)


def get_or_create_author(author_name: str) -> int | None:
    """
    Проверить, существует ли автор с таким именем.
    Если нет, добавляет нового автора.
    """

    author_id = author_crud.get_author_id(author_name)
    if author_id:
        return author_id

    new_author = author_crud.add_entity(author_name)
    return new_author.id
