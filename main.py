from src.database import DataBase
from src.db_manager import DBManager
from src.head_hunter_api import HeadHunterAPI


def main():
    hh_api = HeadHunterAPI()
    company = hh_api.get_company_api(["2ГИС", "СБЕР", "Тинькофф"])
    # print(company)
    # vacancies = hh_api.api_connect("python")
    # print(vacancies)
    database = DataBase()
    param_database = database.config_parser()
    database.create_database("headhunter", param_database)
    database.create_table("headhunter", param_database)
    database.insert_companies("headhunter", param_database, company)
    companies_id = database.get_company_id("headhunter", param_database)
    vacancies = hh_api.get_vacancies_api(companies_id)
    database.insert_vacancies("headhunter", param_database, vacancies)
    db_manager = DBManager()

    company_vacancy_count = db_manager.get_companies_and_vacancies_count("headhunter", param_database)
    print("Компания - количество вакансий")
    for company in company_vacancy_count:
        print(f"{company[0]} - {company[1]} шт.")

    company_vacancy = db_manager.get_all_vacancies("headhunter", param_database)
    print("Компания - количество вакансий")
    for company in company_vacancy:
        print(f"{company[0]} - {company[1]}. Зарплата: {company[2]} - {company[3]}. Ссылка на вакансию: {company[4]}")


if __name__ == "__main__":
    main()
