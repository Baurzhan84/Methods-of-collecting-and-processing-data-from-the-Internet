import requests
import json
from pprint import pprint

'''
1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, 
сохранить JSON-вывод в файле *.json.
'''

main_link = 'https://api.github.com'
user = 'Baurzhan84'

r = requests.get(f'{main_link}/users/{user}/repos')

with open('data.json', 'w') as f:
   json.dump(r.json(), f)

for i in r.json():
   print( i['name'])

'''
2. Изучить список открытых API . Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, 
пройдя авторизацию. Ответ сервера записать в файл.
'''
main_link ='https://api.vk.com/method/users.get'
params = {
    'user_id': '8544036',
    'access_token':"c416c612a81cce2e8ed40b2e947353a886925c7f129fadb65ddb64c80784cdf571555b42e7fc1a5d4a9d2",
    'v':'5.124'
}
response = requests.get(main_link, params=params)
j_data = response.json()
#pprint(j_data)

with open('data_vk.json', 'w') as f:
   json.dump(response.json(), f)

print(f'Имя пользователя {j_data["first_name"]} Фамилия {j_data["last_name"]}')