import requests
import json

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
        self.__params = {"text": name, "period": 1, "per_page": 10}
        response = requests.get(self.__url, self.__params)
        if response.status_code == 200:
            return response.json()
        else:
            return {}


    def get_company_api(self, list_company: list) -> list[dict]:
        """Метод подключения к api.hh.ru и получение списка компаний"""
        company_list = []
        for company in list_company:
            self.__url = "https://api.hh.ru/employers"
            self.__params = {"text": company,
                                 "area": 113,
                                 "only_with_vacancies": True,
                                 "period": 1,
                                 "per_page": 10}
            response = requests.get(self.__url, self.__params)
            if response.status_code == 200:
                result = response.json()
            else:
                result = {}
            if result:
                for company_descript in result["items"]:
                    company_dict = {}
                    company_dict["id"] = company_descript["id"]
                    company_dict["name"] = company_descript["name"]
                    company_dict["alternate_url"] = company_descript["alternate_url"]
                    company_dict["vacancies_url"] = company_descript["vacancies_url"]
                    company_list.append(company_dict)
        return company_list
