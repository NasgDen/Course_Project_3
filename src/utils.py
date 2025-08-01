from configparser import ConfigParser

import requests


def get_company_api(list_company: list) -> list[dict]:
    """Метод подключения к api.hh.ru и получение списка компаний"""
    url = "https://api.hh.ru/employers"
    company_list = []
    for company in list_company:
        params = {"text": company, "area": 113, "only_with_vacancies": True, "period": 1, "per_page": 10}
        response = requests.get(url, params)
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


def get_vacancies_api(companies_id):
    """Метод получает вакансии по id компании с api.hh.ru"""
    vacancies = []
    for url_vacancy in companies_id:
        url = url_vacancy[1]
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
        else:
            result = {}
        if result:
            for vacancy in result["items"]:
                vacancy_dict = {}
                vacancy_dict["vacancy_id"] = vacancy["id"]
                vacancy_dict["name"] = vacancy["name"]
                if vacancy["salary"] is not None:
                    vacancy_dict["salary_from"] = vacancy["salary"]["from"]
                    vacancy_dict["salary_to"] = vacancy["salary"]["to"]
                else:
                    vacancy_dict["salary_from"] = None
                    vacancy_dict["salary_to"] = None
                if vacancy["address"] is not None:
                    vacancy_dict["city"] = vacancy["address"]["city"]
                    vacancy_dict["street"] = vacancy["address"]["street"]
                    vacancy_dict["building"] = vacancy["address"]["building"]
                else:
                    vacancy_dict["city"] = None
                    vacancy_dict["street"] = None
                    vacancy_dict["building"] = None
                vacancy_dict["url"] = vacancy["alternate_url"]
                vacancy_dict["company_id"] = vacancy["employer"]["id"]
                if vacancy["snippet"] is not None:
                    vacancy_dict["requirement"] = vacancy["snippet"]["requirement"]
                    vacancy_dict["responsibility"] = vacancy["snippet"]["responsibility"]
                else:
                    vacancy_dict["requirement"] = None
                    vacancy_dict["responsibility"] = None
                vacancies.append(vacancy_dict)
    return vacancies


def config_parser(filename="database.ini", section="postgresql") -> dict:
    """Метод для чтения конфигурации базы данных из файла и сохранения в словарь"""
    parser = ConfigParser()
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {filename} file")
    return config
