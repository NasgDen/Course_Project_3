import psycopg2


class DBManager:

    # def __init__(self):
    #     pass

    def get_companies_and_vacancies_count(self, database_name: str, params: dict) -> list:
        """Метод получает список всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(dbname=database_name, **params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(
                """SELECT company.name, COUNT(*) AS count_vacancy FROM vacancies
                JOIN company USING(company_id) GROUP BY company.company_id"""
            )
            company_vacancy_count = cur.fetchall()
        conn.commit()
        conn.close()
        return company_vacancy_count

    def get_all_vacancies(self, database_name: str, params: dict) -> list:
        """ Метод получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        conn = psycopg2.connect(dbname=database_name, **params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(
                """SELECT company.name, vacancies.name, salary_from, salary_to, vacancies.url FROM vacancies
                   JOIN company USING(company_id)"""
            )
            company_vacancy = cur.fetchall()
        conn.commit()
        conn.close()
        return company_vacancy

    def get_avg_salary(self, database_name: str, params: dict):
        """ Метод получает среднюю зарплату по вакансиям. """
        conn = psycopg2.connect(dbname=database_name, **params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("SELECT AVG(salary_from) FROM vacancies")
            avg_salary = cur.fetchone()
        conn.commit()
        conn.close()
        return round(avg_salary[0], 2)