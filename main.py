from src.head_hunter_api import HeadHunterAPI
from src.database import DataBase


def main():
    hh_api = HeadHunterAPI()
    vacancies = hh_api.api_connect("python")
    print(vacancies)
    database = DataBase()
    param_database = database.config_parser()
    print(param_database)


if __name__ == "__main__":
    main()
