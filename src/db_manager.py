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
