import scrapy
from scrapy.http import HtmlResponse
from leroy.items import LeroyItem
from scrapy.loader import ItemLoader


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        self.start_urls = [f'https://leroymerlin.ru/search/?sortby=8&tab=products&q={search}']

    def parse(self, response):
        categories_page = response.xpath('//div[@class="plp-card-list"]//a[@slot="picture"]').extract()
        paginator = response.xpath('//div[@class="next-paginator-button-wrapper"]/a/@href').extract_first()

        for link in categories_page:
            yield response.follow(link, callback=self.ads_parse)

        if paginator:
            yield response.follow(paginator, callback=self.parse)

    def ads_parse(self, response: HtmlResponse):  # Тут обрабатываем каждое объвление
        loader = ItemLoader(item=LeroyItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_xpathh('description', "//section[@id='nav-characteristics']//text()")
        loader.add_xpath('photo', '//img[@slot="thumbs"]/@src')
        loader.add_value('link', response.url)

        yield loader.load_item()
