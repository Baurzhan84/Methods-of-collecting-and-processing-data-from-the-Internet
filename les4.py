import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

'https://hh.kz/search/vacancy?clusters=true&enable_snippets=true&text=Python&L_save_area=true&area=40&from=cluster_area&showClusters=true'
params = {
    'clusters':'true',
    'enable_snippets':'true',
    'text':'Python',
    'L_save_area':'true',
    'area':'40',
    'from':'cluster_area',
    'showClusters':'true'
          }

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}
main_link = 'https://hh.kz'
search_link = '/search/vacancy'


while True:
    response = requests.get(main_link + search_link, params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    vacancy_list = soup.find_all('div',{'data-qa': ['vacancy-serp__vacancy']})

    vac_res = main_link
    result = []

    for vacancy in vacancy_list:
        vacancy_data = {}
        vac_name = vacancy.find('a', {'data-qa': ['vacancy-serp__vacancy-title']}).get_text()
        vac_employer = vacancy.find('a', {'data-qa': ['vacancy-serp__vacancy-employer']}).get_text()
        vac_city = vacancy.find('span', {'data-qa': ['vacancy-serp__vacancy-address']}).get_text()
        vac_link = vacancy.find('a', {'class': ['bloko-link HH-LinkModifier']})['href']
        vac_salary = vacancy.find('span', {'data-qa': ['vacancy-serp__vacancy-compensation']})
        try:
            vac_salary = int(vac_salary)
        except:
            vac_salary = None

            vacancy_data['Вакансия'] = vac_name
            vacancy_data['Компания'] = vac_employer
            vacancy_data['Город'] = vac_city
            vacancy_data['зп'] = vac_salary
            result.append(vacancy_data)


    next_link = vacancy.find('a', {'data-qa': ['pager-page']})
    if next_link:
        params['page'] = str(int(params['page'])+1)
    else:
        break
pprint(result)