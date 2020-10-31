import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem_book24


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=%D1%8D%D0%BA%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//div[@class="book__title "]/a/@href').extract()
        next_page = response.xpath("//a[contains(text(),'Далее')]/@href").extract_first()
        for link in links:
            yield response.follow(link, callback=self.book_parse)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        author = response.xpath('//a[@class="item-tab__chars-link js-data-link"]/text()').extract()
        name = response.xpath('//h1/text()').extract()
        price = response.xpath('//div[@class="item-actions__price-old"]/text()').extract_first()
        discount = response.xpath('//b[@itemprop="price"]/text()').extract_first()
        link = response.url

        yield BookparserItem_book24(name=name, price=price, discount=discount, link=link,
                                    author=author)
