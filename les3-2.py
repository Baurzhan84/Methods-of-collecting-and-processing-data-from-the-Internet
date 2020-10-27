import vacancy_search as vs
from pymongo import MongoClient

def data_insert(data):
    n = 0
    for d in data:
        vacancy.insert_one(d)

    n += 1
    print(f'Вставлено новых {n} записей')

key = input('Введите поисковый запрос на hh.kz : ')

vacancy_hh = vs.hhvacancy(key)


client = MongoClient('localhost', 27017)
db = client['vacancys_db']

vacancy = db.vacancys_db

# vacancy.delete_many({})

data_insert(vacancy_hh)

