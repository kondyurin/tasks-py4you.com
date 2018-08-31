# Написать любой парсер с использованием селениума.
#

import random
from lxml import html
from time import sleep
from selenium import webdriver


driver = webdriver.Chrome(executable_path='/Users/anton/PythonProjects/py4seo/chromedriver')
driver.get('https://web.archive.org/')

search_elem = driver.find_element_by_xpath('//*[@id="react-wayback-search"]/div/div[1]/form/div[2]/div/input[1]')

sleep(random.randint(1, 6))
search_elem.send_keys('https://www.YOUR_URL.ru/')
sleep(random.randint(7,8))
# driver.implicitly_wait(20)

source_code = driver.page_source

dom_tree = html.fromstring(source_code)

links = dom_tree.xpath('//*[@id="wb-calendar"]/div/div/div/div/div/div/div/a/@href')

print(links)


# date_lst = driver.find_element_by_xpath('//*[@id="wb-calendar"]/div/div/div/div/div/div/div/a/@href').text
# print(date_lst)