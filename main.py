from src.head_hunter_api import HeadHunterAPI


def main():
    hh_api = HeadHunterAPI()
    vacancies = hh_api.api_connect("python")
    print(vacancies)


if __name__ == "__main__":
    main()
