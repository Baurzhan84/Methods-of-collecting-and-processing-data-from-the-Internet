# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BookparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books2810

    def process_item(self, item, spider):
        if spider.name == 'labirint':
            item['title'], item['currency'] = self.cleaning_procces(item['title'], item['currency'])
            item['old_price'] = float(item['old_price'])
            item['new_price'] = float(item['new_price'])
        elif spider.name == 'book24':
            item['price'], item['discount'] = self.cleaning_procces_books24(item['price'], item['discount'])
            if item['price'] is not None:
                item['price'] = float(item['price'])
            if item['discount'] is not None:
                item['discount'] = float(item['discount'])

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def cleaning_procces(self, title, currency):
        title = str(title).split(":")[1]
        currency = str(currency).replace('.', '')
        return title, currency

    def cleaning_procces_books24(self, price, discount):
        if discount is not None:
            discount = str(discount).replace('р','').replace(' ','')
        if price is not None:
            price = str(price).replace('р','').replace(' ','')
        return price, discount
