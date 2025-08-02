from unittest.mock import patch
from src.utils import get_company_api, get_vacancies_api


@patch("requests.get")
def test_get_company_api(mock_get, company):
    mock_get.return_value.json.return_value = company
    mock_get.return_value.status_code = 200
    result = get_company_api(["company"])
    list_company = [{'alternate_url':
                         'https://hh.ru/employer/64174',
                         'id': '64174',
                         'name': '2ГИС',
                         'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=64174'}]
    assert result == list_company

@patch("requests.get")
def test_get_vacancies_api(mock_get,vacancy):
    mock_get.return_value.json.return_value = vacancy
    mock_get.return_value.status_code = 200
    result = get_vacancies_api([(1,"1")])
    vacancy = [{'building': 'building',
                'city': 'city',
                'company_id': 'employer_id',
                'name': '2ГИС',
                'requirement': 'requirement',
                'responsibility': 'responsibility',
                'salary_from': 100,
                'salary_to': 200,
                'street': 'street',
                'url': 'https://hh.ru/employer/64174',
                'vacancy_id': '64174'}]
    assert result == vacancy
