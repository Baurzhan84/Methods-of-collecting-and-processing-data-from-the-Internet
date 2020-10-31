import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D1%8D%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%BA%D0%B0/?stype=0']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[@class="product-title-link"]/@href').extract()
        next_page = response.xpath('//a[@class="pagination-next__text"]/@href').extract_first()
        for link in links:
            yield response.follow(link, callback=self.book_parse)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        author = response.xpath('//a[@data-event-type="225"]/text()').extract()
        title = response.xpath('//h1/text()').extract()
        old_price = response.xpath('//span[@class="buying-priceold-val-number"]/text()').extract_first()
        new_price = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').extract_first()
        currency = response.xpath('//span[@class="buying-pricenew-val-currency"]/text()').extract_first()
        link = response.url
        yield BookparserItem(title=title, old_price=old_price, new_price=new_price, currency=currency,
                             author=author, link=link)