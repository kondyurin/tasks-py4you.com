# Написать скрипт проверки позиций сайта. Скрипт считывает запросы из файла. Домен задаётся в консоли.
# Результат работы записывается в другой csv файл.
#
# Прокси можно не использовать.
#
# Формат файла результатов:
# Ключ;урл домена;позиция

from requests_html import HTMLSession
import csv

domain_input = input('Введите название домена: ')


def get_data_from_csv():
    """
    Функция считывает данные из файла и преобразует в список.

    """
    keywords_for_checking = []
    with open('in.csv', 'r', encoding='utf-8') as f:
        for line in f:
            keywords_for_checking.append(line.strip().lower())
    return keywords_for_checking


def get_pos_num(keyword, domain):
    """
    Функция получает на вход ключевое слово, домен, возвращает позицию, ключ, url

    """
    session = HTMLSession()
    resp = session.get(f'https://www.google.com/search?q={keyword}&num=10&hl=en')
    links = resp.html.xpath('//*[@id="rso"]/div[1]/div/div/div/div/h3/a/@href')
    for index, link in list(enumerate(links, 1)):
        if domain in link:
            return keyword, link, index


def write_data_to_csv(data):
    """
    Функция получает на вход данные в виде списка кортежей и записывает каждый кортеж построчно в файл

    """
    with open('out.csv', 'w') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)


res_lst = []

for item in get_data_from_csv():
    res = get_pos_num(item, domain_input)
    res_lst.append(res)

write_data_to_csv(res_lst)
