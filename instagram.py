import scrapy
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy


class InstagramSpider(scrapy.Spider):
    # атрибуты класса
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'bbbexeitov'
    insta_pwd = '#PWD_INSTAGRAM_BROWSER:10:1604831128:AfBQABHLdlBUJgEDfr2o6CH0fEO8uks7S9boFBs5g5t6YyclRvWPNXYe2TKZ5jKyGhVGPkB6DyleZb916aP25O6omYzKkZKxqbaDa6u+XLe7CvxDKVL8WEgM+cp70HoCrGkeGGaiPUg/NGFd'
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_start_url = 'https://instagram.com'
    inst_user_link = 'https://instagram.com/' + insta_login + '/'
    parse_user = ['ai_machine_learning', 'dme.aero']  # Пользователь, у которого собираем . Можно указать список

    graphql_url = 'https://www.instagram.com/graphql/query/?'
    hash_follow = 'd04b0a864b4b54837c0d870b0e77e076'  # hash для получения данных по follow
    hash_followers = 'c76146de99bb02f6415203be841dd25a'  # hash для получения данных по followers

    def parse(self, response: HtmlResponse):  # Первый запрос на стартовую страницу
        csrf_token = self.fetch_csrf_token(response.text)  # csrf token забираем из html
        yield scrapy.FormRequest(  # заполняем форму для авторизации
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.insta_login, 'enc_password': self.insta_pwd},
            headers={'X-CSRFToken': csrf_token}
        )

    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            for user in self.parse_user:
                for i in range(2):
                    if i == 0:
                        self.query_hash = self.hash_follow
                        self.follow = True
                        self.followers = False
                        yield response.follow(
                            f'/{user}',
                            callback=self.user_data_parse,
                            cb_kwargs={'username': user})
                    else:
                        self.query_hash = self.hash_followers
                        self.follow = False
                        self.followers = True
                        yield response.follow(
                            f'/{user}',
                            callback=self.user_data_parse,
                            cb_kwargs={'username': user})

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)  # Получаем id пользователя
        variables = {'id': user_id,  # Формируем словарь для передачи даных в запрос
                     'first': 12}  # 12 users. Можно больше (макс. 50)

        url_posts = f'{self.graphql_url}query_hash={self.query_hash}&{urlencode(variables)}'  # Формируем ссылку для получения данных о постах
        yield response.follow(
            url_posts,
            callback=self.user_posts_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)})  # variables ч/з deepcopy во избежание гонок

    def user_posts_parse(self, response: HtmlResponse, username, user_id,
                         variables):  # Принимаем ответ. Не забываем про параметры от cb_kwargs
        j_data = json.loads(response.text)

        if self.follow == True:
            page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
        else:
            page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')

        if page_info.get('has_next_page'):  # Если есть следующая страница
            variables['after'] = page_info['end_cursor']  # Новый параметр для перехода на след. страницу
            url_posts = f'{self.graphql_url}query_hash={self.query_hash}&{urlencode(variables)}'
            yield response.follow(
                url_posts,
                callback=self.user_posts_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )

        if self.follow == True:
            f_users = j_data.get('data').get('user').get('edge_follow').get('edges')
        else:
            f_users = j_data.get('data').get('user').get('edge_followed_by').get('edges')

        for f_user in f_users:  # Перебираем users, собираем данные
            item = InstaparserItem(
                id=user_id,
                user_id=f_user['node']['id'],
                user_name=f_user['node']['username'],
                full_name=f_user['node']['full_name'],
                photos=f_user['node']['profile_pic_url'],
                ph_path=f_user['node']['profile_pic_url'],
                follow=self.follow,
                followers=self.followers
            )
            yield item

    # Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
