from abc import ABC, abstractmethod


class BaseDatabase(ABC):
    """Базовый абстрактный класс, определяющий интерфейс для создания базы данных и таблиц в ней"""

    @abstractmethod
    def connect_database(self, *args, **kwargs):
        """Метод подключение к базе данных"""
        pass

    @abstractmethod
    def create_database(self, *args, **kwargs):
        """Метод создания базы данных"""
        pass

    @abstractmethod
    def create_table(self, *args, **kwargs):
        """Метод создания таблиц в базе данных"""
        pass
