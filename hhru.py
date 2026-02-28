import requests
import json
from datetime import datetime

url = 'https://api.hh.ru/vacancies'
params = {'area': '2', 'text': 'python developer', 'per_page': '7', 'period': '30'}

response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, params=params)

if response.status_code != 200:
    print(f"Ошибка: {response.status_code}")
    exit()

data = response.json()
vacancies = data.get('items', [])

print(f"НАЙДЕНО ВАКАНСИЙ: {data.get('found', 0)}, ПОКАЗАНО: {len(vacancies)}")

parsed_vacancies = []

for i, v in enumerate(vacancies, 1):
    s = v.get('salary')
    if s:
        from_ = s.get('from')
        to_ = s.get('to')
        cur = s.get('currency', 'RUR')
        if from_ and to_:
            salary = f"от {from_} до {to_} {cur}"
        elif from_:
            salary = f"от {from_} {cur}"
        elif to_:
            salary = f"до {to_} {cur}"
        else:
            salary = "Не указана"
    else:
        salary = "Не указана"
    
    vacancy_data = {
        'id': v.get('id'),
        'name': v['name'],
        'company': v['employer']['name'],
        'city': v['area']['name'],
        'salary': salary,
        'experience': v['experience']['name'],
        'employment': v['employment']['name'],
        'schedule': v['schedule']['name'],
        'url': v['alternate_url']
    }
    parsed_vacancies.append(vacancy_data)
    
    print(f"ВАКАНСИЯ №{i}")
    print(f"   Должность: {v['name']}")
    print(f"   Компания: {v['employer']['name']}")
    print(f"   Город: {v['area']['name']}")
    print(f"   Зарплата: {salary}")
    print(f"   Опыт: {v['experience']['name']}")
    print(f"   Тип занятости: {v['employment']['name']}")
    print(f"   График: {v['schedule']['name']}")
    print(f"   Ссылка: {v['alternate_url']}")


output_data = {
    'search_params': {
        'area': 'Санкт-Петербург',
        'query': params['text'],
        'period': f"{params['period']} дней",
        'total_found': data.get('found', 0)
    },
    'vacancies': parsed_vacancies,
    'parsed_at': datetime.now().strftime('%d.%m.%Y %H:%M:%S')
}

filename = f"spb_python_vacancies_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f" Данные сохранены в файл: {filename}")