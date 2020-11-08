# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    id = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    full_name = scrapy.Field()
    photos = scrapy.Field()
    ph_path = scrapy.Field()
    follow = scrapy.Field()
    followers = scrapy.Field()
