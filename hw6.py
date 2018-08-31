# Написать парсер на функциях, без использования классов.
# Аналог Скриминг Фрог Сео Спайдера. Вводишь домен, и
# сканер лезет по всем страницам сайта.
# При этом записывает в файл урл, тайтл, дескрипшен, н1.
# И если находит дубль, помечает, что это дубль в файле.

from requests_html import HTMLSession
from time import sleep


url_visited = []

excluded = ['mailto:', 'favicon', '.ico',  # список стоп-слов для урл
            '.css', '.js', '.jpg',
            '.jpeg', '.png', '.gif',
            '#', '?', '.pdf', '.doc', 'tel:']


def get_data(url):

    """
    На входе урл, на выходе HTML

    """

    session = HTMLSession()
    data = session.get(url)
    sleep(1)
    return data


def get_url_lst(data, url):

    """
    На входе html, на выходе список ссылок

    """

    links_lst = []
    links = list(set(data.html.xpath('//a/@href')))  # ищем все ссылки и удаляем дубликаты
    for link in links:
        if link and link != url and link not in links_lst and not any(word in link for word in excluded):
            if link[:7] == 'http://' or link[:8] == 'https://' or link[:3] == 'www':
                links_lst.append(url)
            elif link[:3] == '../':
                link = link[3:]
            elif link[:2] == './':
                link = link[2:]
            elif link[0] == '/':
                link = link[1:]
            else:
                links_lst.append(f'{url}{link}')
    return links_lst


def do_crawl(url, depth=1, max_depth=2):
    """
    На входе url, глубина прохода, макс глубина прохода вглубь
    На выходе список пройденных url

    """

    url_visited.append(url)  # очередь пройденных url , list

    if depth > max_depth:
        return
    html = get_data(url)
    urls = get_url_lst(html, url)

    for url in urls:
        if url in url_visited:
            continue
        do_crawl(url, depth + 1)

    return url_visited


def get_elem(urls_lst):

    """
    На входе список пройденных url
    На выходе значения тегов

    """

    for item in urls_lst:
        html = get_data(item)
        title = html.html.xpath('//title/text()')
        desc = html.html.xpath('//meta[@name="description"]/@content')
        h1 = html.html.xpath('//h1/text()')
        print(f'{item}: {title}, {desc}, {h1}')


# def write_data_to_csv():
#     """
#     Функция получает на вход данные в виде списка кортежей и
#     записывает каждый кортеж построчно в файл
#
#     """
#     with open('out.csv', 'w') as f:
#         writer = csv.writer(f)
#         for row in data:
#             writer.writerow(row)


if __name__ == '__main__':
    # try:
    while True:
        domain_url = input('Введите домен для анализа: ').strip()
        if domain_url[:7] == 'http://' or domain_url[:8] == 'https://':
            res = do_crawl(domain_url)
            abc = get_elem(res)
            print(abc)
        else:
            print('Введите протокол домена')

