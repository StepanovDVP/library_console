from typing import Callable


class Router:
    def __init__(self):
        self.routes = []

    def filter(self, condition: Callable):
        """
        Декоратор для регистрации функций как маршрутов.
        """

        def decorator(func):
            self.routes.append((condition, func))
            return func

        return decorator

    def handle(self, command: str):
        """
        Выполняет обработку команды.
        """
        for condition, func in self.routes:
            if condition(command):
                func()
                return
        print(f'Команда "{command}" не найдена. Попробуйте снова.')
