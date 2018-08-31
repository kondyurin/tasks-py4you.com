# Написать любой парсер с использованием селениума.


import os
import random
from lxml import html
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = input('Enter URL: ')

img_count = int(input('Enter screenshot count: '))


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


driver = webdriver.Chrome(executable_path='/Users/anton/PythonProjects/py4seo/chromedriver')
driver.get('https://web.archive.org/')

search_elem = driver.find_element_by_xpath('//*[@id="react-wayback-search"]/div/div[1]/form/div[2]/div/input[1]')
sleep(random.randint(1, 3))
search_elem.send_keys(url)
sleep(random.randint(7, 8))

# driver.implicitly_wait(5)

# try:
#     wait = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "wb-calendar"))
#     )
#
# finally:
#     driver.quit()

source_code = driver.page_source

dom_tree = html.fromstring(source_code)

links = dom_tree.xpath('//*[@id="wb-calendar"]/div/div/div/div/div/div/div/a/@href')

res_lst = ['https://web.archive.org' + link for link in links]

createFolder('./screenshots/')

for i, l in list(enumerate(res_lst[0:img_count])):
    driver.get(l)
    driver.save_screenshot(f'./screenshots/{i+1}.png')


