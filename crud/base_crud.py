from abc import ABC, abstractmethod
from typing import Type, TypeVar

from file_manager import JSONFileManager
from models.models import Base

ModelType = TypeVar('ModelType', bound=Base)


class CRUDBase(ABC):
    """Базовый класс для управления сущностями."""

    def __init__(self, file_manager_: JSONFileManager, model: Type[ModelType]):
        self.file_manager = file_manager_
        self.model = model
        self.data = self.file_manager.load_data()

    @abstractmethod
    def add_entity(self, **kwargs):
        """Метод добавления новой сущности."""
        pass

    def _increment_id(self) -> int:
        """Возвращает новый ID для следующей сущности."""
        current_id = self.data['current_id'] + 1
        self.data['current_id'] = current_id
        return current_id

    def _save(self):
        """Сохраняет данные в файл."""
        self.file_manager.save_data(self.data)
