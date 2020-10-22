from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['news_db']
news_get = db.news_db

news_get.delete_many({})


def db_news_update(data):
    news_get.update(data, {'upsert': True})

def lenta_news():
     header = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
          }
     lenta_link = 'https://lenta.ru/'
     response = requests.get(lenta_link, headers=header)
     dom = html.fromstring(response.text)
     lenta_news = dom.xpath('//time[@class="g-time"]/../..')

     lenta_list = []
     l = 0
     for n in lenta_news:
          lenta_data = {}
          name = str(n.xpath('.//a/text()')[0]).replace('\\xa0',' ')
          time = str(n.xpath('.//time[@class="g-time"]/text()')[0])
          link = n.xpath('./a/@href')

          lenta_data['name'] = name
          lenta_data['link'] = lenta_link + str(link[0])
          lenta_data['source'] = str("Лента")
          lenta_data['time'] = time
          lenta_data['web-site'] = lenta_link

          lenta_list.append(lenta_data)
          db_news_update(lenta_data)
          l += 1

     print(f'Обработано {l} новостей с {lenta_link}')
     news_get.insert_many(lenta_list)

     return lenta_list

def mail_news():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    }
    mailru_link = 'https://news.mail.ru/'
    response = requests.get(mailru_link, headers=header)
    dom = html.fromstring(response.text)

    news_data = []
    items = dom.xpath("//div[@class='newsitem newsitem_height_fixed js-ago-wrapper']")
    l = 0
    for item in items:
        data = item.xpath("./..//text()")
        link = item.xpath(".//@href")
        time = str(item.xpath('.//@datetime')[0])
        source = data[2]
        for d in range(3, len(data)):
            news = {}
            if d != 4:
                news['name'] = str(data[d]).replace('\xa0', ' ')
                news['link'] = mailru_link + str(link[0])
                news['source'] = source
                news['time'] = time
                news['web-site'] = mailru_link
                # news['news_data'] = data
                # pprint(news)
                news_data.append(news)
                # db_news_update(news)
                l += 1

    print(f'Обработано {l} новостей с {mailru_link}')
    news_get.insert_many(news_data)

    return news_data





def yandex_news():

     header = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
     }
     yandex_link = 'https://yandex.kz/news'
     response = requests.get(yandex_link, headers=header)
     dom = html.fromstring(response.text)
     yandex_news = dom.xpath('//div[@class="mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top"]//article')

     yandex_list = []
     l = 0

     for yandex in yandex_news:
          yandex_data = {}
          name = str(yandex.xpath('.//h2[@class="news-card__title"]/text()')[0])
          # pprint(name)
          link = str(yandex.xpath('.//a[@class="news-card__link"]/@href'))
          time = str(yandex.xpath('.//span[@class="mg-card-source__time"]/text()')[0])
          source =str(yandex.xpath('.//span[@class="mg-card-source__source"]/a/text()')[0])

          yandex_data['name'] = name
          yandex_data['link'] = yandex_link + str(link[1])
          yandex_data['time'] = time
          yandex_data['source'] = source
          yandex_data['web-site'] = yandex_link

          yandex_list.append(yandex_data)
          db_news_update(yandex_data)
          l += 1

     print(f'Обработано {l} новостей с {yandex_link}')
     news_get.insert_many(yandex_list)

     return yandex_list

lenta_news()
mail_news()
yandex_news()


