import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re

def hhvacancy(key):
    main_link = 'https://hh.kz'
    search_link = '/search/vacancy'

    search = key
    n = 0
    lnum = 0

    while True:
        params = {
            'clusters':'true',
            'area': '40',
            'enable_snippets': 'true',
            'salary': '',
            'st' : 'searchVacancy',
            'text': search}

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
            }
        response = requests.get(main_link + search_link, params=params, headers=headers)
        soup = bs(response.text, 'html.parser')
        vacancy_list = soup.find_all('div', {'class': ['vacancy-serp-item']})

        vac_res = main_link
        result = []

        for vacancy in vacancy_list:
            vacancy_data = {}
            vac_name = vacancy.find('a', {'data-qa': ['vacancy-serp__vacancy-title']}).get_text()
            vac_employer = vacancy.find('a', {'data-qa': ['vacancy-serp__vacancy-employer']}).get_text()
            vac_city = vacancy.find('span', {'data-qa': ['vacancy-serp__vacancy-address']}).get_text()
            vac_link = vacancy.find('a', {'class': ['bloko-link HH-LinkModifier']})['href']
            vac_salary = vacancy.find('span', {'data-qa': ['vacancy-serp__vacancy-compensation']})
            vac_salary_min = None
            vac_salary_max = None
            salary_currency = None

            if vac_salary:

                vac_salary = vac_salary.getText() \
                    .replace(u'\xa0', u'')
                vac_salary = re.split(r'\s|-', vac_salary)

                if vac_salary[0] == 'до':
                    vac_salary_max = int(vac_salary[1])
                elif vac_salary[0] == 'от':
                    vac_salary_min = int(vac_salary[1])
                else:
                    vac_salary_min = int(vac_salary[0])
                    vac_salary_max = int(vac_salary[1])

            vacancy_data['Вакансия'] = vac_name
            vacancy_data['Компания'] = vac_employer
            vacancy_data['Город'] = vac_city
            vacancy_data['зп_мин'] = vac_salary_min
            vacancy_data['зп_макс'] = vac_salary_max
            vacancy_data['Сайт'] = vac_res
            result.append(vacancy_data)
            lnum += 1

            try:
                next_button = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'}).getText()
                n += 1
                # break
            except:
                print(f'Всего найдено {lnum} записей c hh.kz')
                break

        return result