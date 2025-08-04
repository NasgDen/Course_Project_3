from src.db_manager import DbManager
from src.utils import config_parser, get_company_api, get_vacancies_api


def main():
    """Основная точка входа"""
    company = (input("Введите список компаний, через запятую, для создания базы данных: ")).split(",")
    # Поиск названий компаний через api.hh.ru
    company_api = get_company_api(company)
    # Сохранение настроек подключения к базе данных из файла database.ini в переменную config_db
    config_db = config_parser()
    # Создание экземпляра класса DbManager
    head_hunter_db = DbManager("headhunter", config_db)
    # Создание базы данных
    head_hunter_db.create_database()
    # Создание таблиц company и vacancies в базе данных.
    head_hunter_db.create_table(config_db)
    # Заполнение значениями таблицу company
    head_hunter_db.insert_companies(company_api)
    # Получение ссылки на вакансии компаний
    url_vacancy = head_hunter_db.get_company_id()
    # Получение списка вакансий компаний
    vacancy_api = get_vacancies_api(url_vacancy)
    # Заполнение значениями таблицу vacancies
    head_hunter_db.insert_vacancies(vacancy_api)
    # Вывод количества вакансий у каждой компании
    company_vacancy_count = head_hunter_db.get_companies_and_vacancies_count()
    print("Компания - количество вакансий")
    for company in company_vacancy_count:
        print(f"{company[0]} - {company[1]} шт.")
    # Вывод всех вакансий компаний
    company_vacancy = head_hunter_db.get_all_vacancies()
    print("Компания - количество вакансий")
    for company in company_vacancy:
        print(f"{company[0]} - {company[1]}. Зарплата: {company[2]} - {company[3]}. Ссылка на вакансию: {company[4]}")
    # Подсчет средней зарплаты по вакансиям
    avg_salary = head_hunter_db.get_avg_salary()
    print(f"Средняя зарплата по вакансиям {avg_salary} руб.")
    # Вывод списка вакансий у которых зарплата больше средней
    vacancy_avg_salary = head_hunter_db.get_vacancies_with_higher_salary(avg_salary)
    print("Вакансии у которых зарплата больше средней")
    for vacancy in vacancy_avg_salary:
        print(f"{vacancy[0]} - {vacancy[1]}. Зарплата: {vacancy[2]}. Ссылка на вакансию: {vacancy[3]}")
    # Поиск по вакансиям
    keyword = input("Введите слова для поиска вакансий: ").split(",")
    vacancies_with_keyword = head_hunter_db.get_vacancies_with_keyword(keyword)
    for vacancy in vacancies_with_keyword:
        print(f"{vacancy[0]} - {vacancy[1]}. Зарплата: {vacancy[2]}. Ссылка на вакансию: {vacancy[3]}")


if __name__ == "__main__":
    main()
