import psycopg2

from src.base_database import BaseDatabase


class DbManager(BaseDatabase):
    """Класс, определяющий интерфейс для создания базы данных и таблиц в ней"""

    def __init__(self, database_name, params):
        self.conn = psycopg2.connect(dbname="postgres", **params)
        self.cur = self.conn.cursor()
        self.database_name = database_name

    def create_database(self) -> None:
        """Метод создания базы данных"""
        self.conn.autocommit = True
        with self.conn.cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS {self.database_name}")
            cur.execute(f"CREATE DATABASE {self.database_name}")
            self.conn.commit()

    def create_table(self, params) -> None:
        """Метод создания таблиц в базе данных"""
        self.conn = psycopg2.connect(dbname=self.database_name, **params)
        self.conn.autocommit = True
        with self.conn.cursor() as cur:
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
                    city VARCHAR(250),
                    street VARCHAR(250),
                    building VARCHAR(250),
                    url VARCHAR(250),
                    company_id INTEGER REFERENCES company (company_id),
                    requirement TEXT,
                    responsibility TEXT
                )
            """
            )
        self.conn.commit()

    def insert_companies(self, companies: list) -> None:
        """Метод заполняет таблице company значениями полученными из api.hh.ru"""
        # self.conn.autocommit = True
        with self.conn.cursor() as cur:
            for company in companies:
                cur.execute(
                    "INSERT INTO company(company_id, name, url, vacancies_url) VALUES (%s, %s, %s, %s)",
                    (company["id"], company["name"], company["alternate_url"], company["vacancies_url"]),
                )
            self.conn.commit()

    def insert_vacancies(self, vacancies: list) -> None:
        """Метод заполняет таблице vacancy значениями полученными из api.hh.ru"""
        with self.conn.cursor() as cur:
            for vacancy in vacancies:
                cur.execute(
                    """INSERT INTO vacancies
                    (
                    vacancy_id,
                    name,
                    salary_from,
                    salary_to,
                    city,
                    street,
                    building,
                    url,
                    company_id,
                    requirement,
                    responsibility
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (
                        vacancy["vacancy_id"],
                        vacancy["name"],
                        vacancy["salary_from"],
                        vacancy["salary_to"],
                        vacancy["city"],
                        vacancy["street"],
                        vacancy["building"],
                        vacancy["url"],
                        vacancy["company_id"],
                        vacancy["requirement"],
                        vacancy["responsibility"],
                    ),
                )
            self.conn.commit()

    def get_company_id(self) -> list:
        """Метод сохраняет значения параметров company_id и vacancies_url в кортеж"""
        with self.conn.cursor() as cur:
            cur.execute("SELECT company_id, vacancies_url FROM company")
            company_id = cur.fetchall()
        return company_id

    def get_companies_and_vacancies_count(self) -> list:
        """Метод получает список всех компаний и количество вакансий у каждой компании."""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT company.name, COUNT(*) AS count_vacancy FROM vacancies
                JOIN company USING(company_id) GROUP BY company.company_id"""
            )
            company_vacancy_count = cur.fetchall()
        return company_vacancy_count

    def get_all_vacancies(self) -> list:
        """Метод получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT company.name, vacancies.name, salary_from, salary_to, vacancies.url FROM vacancies
                   JOIN company USING(company_id)"""
            )
            company_vacancy = cur.fetchall()
        return company_vacancy

    def get_avg_salary(self) -> float:
        """Метод получает среднюю зарплату по вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute("SELECT AVG(salary_from) FROM vacancies")
            avg_salary = cur.fetchone()
        return round(avg_salary[0], 2)

    def get_vacancies_with_higher_salary(self, avg_salary: float):
        """Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute(
                f"""SELECT company.name, vacancies.name, salary_from, vacancies.url FROM vacancies
                   JOIN company USING(company_id)
                   WHERE salary_from > {avg_salary}"""
            )
            vacancy_avg_salary = cur.fetchall()
        return vacancy_avg_salary

    def get_vacancies_with_keyword(self, keywords: list[str]) -> list:
        """Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        vacancies_with_keyword = []
        with self.conn.cursor() as cur:
            for keyword in keywords:
                cur.execute(
                    f"""SELECT company.name, vacancies.name, salary_from, vacancies.url FROM vacancies
                       JOIN company USING(company_id)
                       WHERE LOWER(company.name) LIKE LOWER('%{keyword}%')
                       OR LOWER(vacancies.name) LIKE LOWER('%{keyword}%')"""
                )
                vacancy = cur.fetchall()
                vacancies_with_keyword.extend(vacancy)
        return vacancies_with_keyword
