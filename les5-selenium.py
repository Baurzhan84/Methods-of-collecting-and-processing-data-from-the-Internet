from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from pprint import pprint
from pymongo import MongoClient

import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome('./chromedriver.exe', options=chrome_options)

driver.get('https://e.mail.ru/inbox/0:16034585540637004177:0/')
time.sleep(5)

login = driver.find_element_by_name('username')
login.send_keys('study.ai_172@mail.ru')
login.send_keys(Keys.ENTER)
time.sleep(5)

password = driver.find_element_by_name('password')
password.send_keys('NextPassword172')
password.send_keys(Keys.ENTER)
mails_num = 1
while True:
    try:
        time.sleep(5)
        button = driver.find_element_by_xpath(
            '//span[@class="button2 button2_has-ico button2_arrow-down button2_pure button2_short '
            'button2_ico-text-top button2_hover-support js-shortcut"]')
        button.click()

    except:
        print(f'error  from at the {mails_num}')
        break

    mails = driver.find_elements_by_class_name('scrollable__container')
    mail_data = []
    mails_num = 1

    for m in mails:
        mail_list = {}
        title = str(m.find_element_by_xpath('//h2[@class="thread__subject"]').text)

        sender = str(m.find_element_by_xpath('//span[@class="letter-contact"]').text)
        date = str(m.find_element_by_xpath('//div[@class="letter__date"]').text)

        mail_list['title'] = title
        mail_list['sender'] = sender
        mail_list['date'] = date

        if mail_list not in mail_data:
            mail_data.append(mail_list)
            mails_num += 1
            pprint(mail_data)
            driver.quit()

        client = MongoClient('localhost', 27017)
        db = client['emails_db']
        email_get = db.emails_db

        email_get.delete_many({})
        email_get.insert_many(mail_list)
