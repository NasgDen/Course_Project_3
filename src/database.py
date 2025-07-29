import psycopg2
from configparser import ConfigParser

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

    def create_database(self, database_name: str, params: dict):
        """Метод создания базы данных"""
        conn = psycopg2.connect(dbname="postgres", **params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
            cur.execute(f"CREATE DATABASE {database_name}")
        conn.commit()
        conn.close()

    @staticmethod
    def create_table(database_name: str, params: dict):
        """Метод создания таблиц в базе данных"""
        conn = psycopg2.connect(dbname=database_name, **params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(f"""
                CREATE TABLE company(
                    company_id SERIAL PRIMARY KEY,
                    name VARCHAR(250),
                    address VARCHAR(250)
                )
            """)
            cur.execute(f"""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    name VARCHAR(250),
                    salary_from INTEGER,
                    salary_to INTEGER,
                    company_id INTEGER REFERENCES company (company_id)
                )
            """)
        conn.commit()
        conn.close()
