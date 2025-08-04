import pytest


@pytest.fixture()
def company():
    return {  'items': [
    {
      'alternate_url': 'https://hh.ru/employer/64174',
      'id': '64174',
      'logo_urls': {
        '240': 'https://img.hhcdn.ru/employer-logo/5688469.jpeg',
        '90': 'https://img.hhcdn.ru/employer-logo/5688468.jpeg',
        'original': 'https://img.hhcdn.ru/employer-logo-original/1016925.jpeg'
      },
      'name': '2ГИС',
      'open_vacancies': 253,
      'url': 'https://api.hh.ru/employers/64174',
      'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=64174'
    }]}

@pytest.fixture()
def vacancy():
    return {  'items': [
    {
      'alternate_url': 'https://hh.ru/employer/64174',
      'id': '64174',
      'logo_urls': {
        '240': 'https://img.hhcdn.ru/employer-logo/5688469.jpeg',
        '90': 'https://img.hhcdn.ru/employer-logo/5688468.jpeg',
        'original': 'https://img.hhcdn.ru/employer-logo-original/1016925.jpeg'
      },
      'name': '2ГИС',
      'open_vacancies': 253,
      'url': 'https://api.hh.ru/employers/64174',
      'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=64174',
      'salary':{
          'from': 100,
          'to': 200
      },
        'address':{
            'city': 'city',
            'street': 'street',
            'building': 'building'
        },
        'employer':{
            'id': 'employer_id'
        },
        'snippet':{
            'requirement': 'requirement',
            'responsibility': 'responsibility'
        }
    }]}



