from src.database import DataBase
from src.head_hunter_api import HeadHunterAPI


def main():
    hh_api = HeadHunterAPI()
    company = hh_api.get_company_api(["СБЕР", "2ГИС"])
    print(company)
    # vacancies = hh_api.api_connect("python")
    # print(vacancies)
    database = DataBase()
    param_database = database.config_parser()
    database.create_database("headhunter", param_database)
    database.create_table("headhunter", param_database)


if __name__ == "__main__":
    main()
