import requests

from src.base_api import BaseApiClass


class HeadHunterAPI(BaseApiClass):
    """Класс для работы с api.hh.ru"""

    __url = "https://api.hh.ru/vacancies"
    __params: dict = {}

    def __init__(self):
        """Инициализация атрибутов класса"""
        pass

    def api_connect(self, name):
        """Метод подключения к api.hh.ru"""
        self.__params = {"text": name, "period": 60, "per_page": 100}
        response = requests.get(self.__url, self.__params)
        if response.status_code == 200:
            return response.json()
        else:
            return {}
