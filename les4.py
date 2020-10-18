import requests
from bs4 import BeautifulSoup as bs
result = []

params = {
        'clusters': 'true',
        'area': '160',
        'enable_snippets' : 'true',
        'salary': '',
        'st': 'searchVacancy',
        'text': ''
}

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}

link = 'https://hh.kz/search/vacancy'


while True:
    response = requests.get(link, params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    vacancy_list = soup.findAll('div', {'class': ['vacancy-serp-item']})
    vac_res = link

    for vacancy in vacancy_list:
        vac_name = vacancy.find('a', {'data-qa': ['vacancy-serp__vacancy-title']}).get_text
        vac_salary = vacancy.find('span', {'data-qa': ['vacancy-serp__vacancy-compensation']})
        vac_min_salary = None
        vac_max_salary = None
        if vac_salary:
            if vac_salary.text.find('от') != -1:
                vac_min_salary = vac_salary.text.split('')[1]
            if vac_salary.text.find('до') != -1:
                vac_max_salary = vac_salary.text.split('')[1]
            if vac_salary.text.find('-') != -1:
                vac_min_salary = vac_salary.text.split('')[0]
                vac_max_salary = vac_salary.text.split('')[1]

    vac_employer = vacancy.find('a', {'data-qa': ['vacancy-serp__vacancy-employer']})
    vac_city = vacancy.find('span', {'data-qa': ['vacancy-serp__vacancy-compensation']})
    vac_link = vacancy.find('a', ['bloko-link HH-LinkModifier'])
    result.append({'name': vac_name,
                   'min salary': vac_min_salary,
                   'max salary': vac_max_salary,
                   'employer': vac_employer.text,
                   'place': vac_city,
                   'link': vac_res})

    next_link = soup.find('a', {'data-qa': ['pager-next']})
    if next_link:
        params['page'] = str(int(params['page'])+1)
    else:
        break