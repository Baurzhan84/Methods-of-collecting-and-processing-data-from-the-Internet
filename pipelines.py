# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import os
from urllib.parse import urlparse

import scrapy
from pymongo import MongoClient


class DataBasePipeline:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.mongo_base = self.client.insta

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def __del__(self):
        self.client.close()

class InstaPhotoline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            try:
                yield scrapy.Request(item['photos'], meta=item)
            except Exception as e:
                print(e)

    def file_path(self, request, response=None, info=None):
        if request.meta['follow'] == True:
            media_dir = os.path.basename('follow')
        else:
            media_dir = os.path.basename('followers')
        media_name = os.path.basename(request.meta['user_name'])
        dir = '/full/%s/%s' % (media_dir, media_name)
        return dir