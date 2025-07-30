from configparser import ConfigParser

import psycopg2

from src.base_database import BaseDatabase


class DataBase(BaseDatabase):
    """Класс, определяющий интерфейс для создания базы данных и таблиц в ней"""

    # def __init__(self):

    @staticmethod
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

    def connect_database(self, database_name: str, params: dict):
        """Метод подключение к базе данных"""
        pass

    def create_database(self, database_name: str, params: dict) -> None:
        """Метод создания базы данных"""
        conn = psycopg2.connect(dbname="postgres", **params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
            cur.execute(f"CREATE DATABASE {database_name}")
        conn.commit()
        conn.close()

    @staticmethod
    def create_table(database_name: str, params: dict) -> None:
        """Метод создания таблиц в базе данных"""
        conn = psycopg2.connect(dbname=database_name, **params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE company(
                    company_id INTEGER PRIMARY KEY,
                    name VARCHAR(250),
                    url VARCHAR(250),
                    vacancies_url VARCHAR(250)
                )
            """
            )
            cur.execute(
                """
                CREATE TABLE vacancies (
                    vacancy_id INTEGER PRIMARY KEY,
                    name VARCHAR(250),
                    salary_from INTEGER,
                    salary_to INTEGER,
                    company_id INTEGER REFERENCES company (company_id)
                )
            """
            )
        conn.commit()
        conn.close()

    @staticmethod
    def insert_companies(database_name: str, params: dict, companies: list) -> None:
        """ Метод заполняет таблице company значениями полученными из api.hh.ru """
        conn = psycopg2.connect(dbname=database_name, **params)
        conn.autocommit = True
        for company in companies:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO company(company_id, name, url, vacancies_url) VALUES (%s, %s, %s, %s)""",
                    (company["id"], company["name"], company["alternate_url"], company["vacancies_url"])
                )
        conn.commit()
        conn.close()

    @staticmethod
    def get_company_id(database_name: str, params: dict):
        pass
