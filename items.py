# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field()
    title = scrapy.Field()
    old_price = scrapy.Field()
    new_price = scrapy.Field()
    currency = scrapy.Field()
    link = scrapy.Field()
    _id = scrapy.Field()
    pass


class BookparserItem_book24(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    discount = scrapy.Field()
    link = scrapy.Field()
    _id = scrapy.Field()
    pass
