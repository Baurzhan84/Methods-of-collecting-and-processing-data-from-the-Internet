from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['vacancys_db']

vacancy = db.vacancys_db

for v in vacancy.find({'salary_min': {'$gt': 150000}, 'salary_max': {'$lt': 200000}, 'web-site': 'www.hh.ru'},
                      {'name': 1, 'salary_min': 1, 'salary_max': 1, 'salary_cur': 1, 'link': 1, '_id': 0}):
    print(v)
