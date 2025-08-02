import psycopg2

from unittest.mock import patch
from src.db_manager import DbManager

@patch("psycopg2.connect")
def test_dbmanager(mock_connect):
    mock_conn = mock_connect.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchone.return_value = ("mocked_data",)
    params = {"test": "test"}
    test_db = DbManager("test", params)
    mock_connect.assert_called_once()

    assert test_db.create_database() == None
    mock_connect.assert_called()
    assert test_db.create_table(params) == None
    mock_connect.assert_called()

    company = [{"id": 1, "name": "Comp_test", "alternate_url": "www.test.ru", "vacancies_url": "www.test.ru"}]
    assert test_db.insert_companies(company) == None
    mock_connect.assert_called()

    vacancies = [{"vacancy_id": 12,
                  "name": "Vac_1",
                  "salary_from": 1,
                  "salary_to": 2,
                  "city": "city",
                  "street": "street",
                  "building": "building",
                  "url": "url",
                  "company_id": 1,
                  "requirement": "requirement",
                  "responsibility": "responsibility"}]
    assert test_db.insert_vacancies(vacancies) == None
    mock_connect.assert_called()


