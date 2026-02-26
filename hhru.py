import requests
import json
from datetime import datetime

url = 'https://api.hh.ru/vacancies'

headers = {'User-Agent': 'Mozilla/5.0'}

params = {
    'area': '2', 
    'text': 'python developer',  
    'per_page': '20',  
    'period': '30', 
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    vacancies = data.get('items', [])
    
    print(f"Найдено вакансий: {data.get('found', 0)}")
    print(f"Показано: {len(vacancies)}")
    
    parsed_vacancies = []
    
    for i, v in enumerate(vacancies, 1):
        salary_info = v.get('salary')
        if salary_info:
            salary_from = salary_info.get('from')
            salary_to = salary_info.get('to')
            salary_currency = salary_info.get('currency', 'RUR')
            
            if salary_from and salary_to:
                salary_text = f"{salary_from} - {salary_to} {salary_currency}"
            elif salary_from:
                salary_text = f"от {salary_from} {salary_currency}"
            elif salary_to:
                salary_text = f"до {salary_to} {salary_currency}"
            else:
                salary_text = "Не указана"
        else:
            salary_text = "Не указана"
        

        vacancy_data = {
            'id': v.get('id'),
            'name': v.get('name'),
            'company': v.get('employer', {}).get('name'),
            'company_url': v.get('employer', {}).get('alternate_url'),
            'city': v.get('area', {}).get('name'),
            'salary': salary_text,
            'experience': v.get('experience', {}).get('name'),
            'employment': v.get('employment', {}).get('name'),
            'schedule': v.get('schedule', {}).get('name'),
            'description': v.get('snippet', {}).get('responsibility'),
            'requirements': v.get('snippet', {}).get('requirement'),
            'url': v.get('alternate_url')
        }
        
        parsed_vacancies.append(vacancy_data)
        
        print(f"\n{i}. {v['name']}")
        print(f"{v['employer']['name']}")
        print(f"Зарплата {salary_text}")
        print(f"{v['area']['name']}")
        print(f"Опыт{v['experience']['name']}")
        print(f"{v['alternate_url']}")
    

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
    print(f" Всего обработано вакансий: {len(parsed_vacancies)}")
    
else:
    print(f" Ошибка: {response.status_code}")