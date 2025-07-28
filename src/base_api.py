from abc import ABC, abstractmethod


class BaseApiClass(ABC):
    """Базовый абстрактный, определяющий интерфейс для работы с api запросами"""

    @abstractmethod
    def api_connect(self, *args, **kwargs):
        """Метод подключения к api hh.ru"""
        pass
