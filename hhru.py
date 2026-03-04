import requests
import json
from datetime import datetime

URL = 'https://api.hh.ru/vacancies'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
PARAMS = {
    'area': '2',
    'text': 'python developer',
    'per_page': '7',
    'period': '30'
}


def parse_salary(salary_data):
    if not salary_data:
        return "Не указана"

    from_sal = salary_data.get('from')
    to_sal = salary_data.get('to')
    currency = salary_data.get('currency', 'RUB')

    if from_sal and to_sal:
        return f"от {from_sal} до {to_sal} {currency}"
    elif from_sal:
        return f"от {from_sal} {currency}"
    elif to_sal:
        return f"до {to_sal} {currency}"
    else:
        return "Не указана"


def main():
    response = requests.get(URL, headers=HEADERS, params=PARAMS)

    if response.status_code != 200:
        print(f"Ошибка: {response.status_code}")
        return

    data = response.json()
    vacancies = data.get('items', [])
    total_found = data.get('found', 0)

    print(f"НАЙДЕНО ВАКАНСИЙ: {total_found}, ПОКАЗАНО: {len(vacancies)}")

    parsed_vacancies = []

    for i, vacancy in enumerate(vacancies, 1):
        salary = parse_salary(vacancy.get('salary'))

        vacancy_data = {
            'id': vacancy.get('id'),
            'name': vacancy['name'],
            'company': vacancy['employer']['name'],
            'city': vacancy['area']['name'],
            'salary': salary,
            'experience': vacancy['experience']['name'],
            'employment': vacancy['employment']['name'],
            'url': vacancy['alternate_url']
        }
        parsed_vacancies.append(vacancy_data)

        print(f"ВАКАНСИЯ №{i}")
        print(f"   Должность: {vacancy['name']}")
        print(f"   Компания: {vacancy['employer']['name']}")
        print(f"   Город: {vacancy['area']['name']}")
        print(f"   Зарплата: {salary}")
        print(f"   Опыт: {vacancy['experience']['name']}")
        print(f"   Тип занятости: {vacancy['employment']['name']}")
        print(f"   Ссылка: {vacancy['alternate_url']}")

    output_data = {
        'search_params': {
            'area': 'Санкт-Петербург',
            'query': PARAMS['text'],
            'period': f"{PARAMS['period']} дней",
            'total_found': total_found
        },
        'vacancies': parsed_vacancies,
    }

    filename = "vacancies.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"Данные сохранены в файл: {filename}")


if __name__ == "__main__":
    main()