from abc import ABC, abstractmethod


class FileHandler(ABC):
    @abstractmethod
    def load_data(self) -> dict:
        pass

    @abstractmethod
    def save_data(self, data: dict):
        pass
