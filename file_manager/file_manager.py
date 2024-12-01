import json
from json import JSONDecodeError

from constant import FILE_PATH_AUTHORS, FILE_PATH_BOOKS
from db.db_json_structure import (
    db_json_structure_for_author, db_json_structure_for_book
)

from .base import FileHandler


class JSONFileManager(FileHandler):
    """Класс для работы с файлами."""

    def __init__(self, file_path: str, file_data: dict):
        self.file_path = file_path
        self.file_data = file_data

    def load_data(self) -> dict:
        """Загружает данные из JSON файла."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                data['elements'] = {
                    int(k): v for k, v in data['elements'].items()
                }
                return data
        except FileNotFoundError:
            return self.file_data
        except JSONDecodeError as e:
            print('Ошибка json file', str(e))
            exit(0)

    def save_data(self, data: dict):
        """Сохраняет данные в JSON файл."""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


json_file_books_manager = JSONFileManager(
    FILE_PATH_BOOKS, db_json_structure_for_book
)

json_file_authors_manager = JSONFileManager(
    FILE_PATH_AUTHORS, db_json_structure_for_author
)
