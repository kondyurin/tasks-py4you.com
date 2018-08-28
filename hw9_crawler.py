# Задача:
# Доделать все тот же многопоточный парсер, только можно без класса.
# Просто на 2-х функциях: одна является обработчиком, именно она
# работает многопоточно, а вторая - стартует потоки.


from requests_html import HTMLSession
from time import sleep
from hw9_db import domain, engine
from threading import Lock
from queue import Queue
from concurrent.futures import ThreadPoolExecutor


url_visited = set()
locker = Lock()
scanned_urls = set()
q = Queue()


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
            if link.startswith('http://') or link.startswith('https://') or link.startswith('www'):
                links_lst.append(url)
            elif link.startswith('../'):
                link = link[3:]
            elif link.startswith('./'):
                link = link[2:]
            elif link.startswith('/'):
                link = link[1:]
            else:
                links_lst.append(f'{url}{link}')
    return links_lst


def do_crawl(url, depth=1, max_depth=1):
    """
    На входе url, глубина прохода, макс глубина прохода вглубь
    На выходе список пройденных url

    """

    url_visited.add(url)  # очередь пройденных url , list

    if depth > max_depth:
        return
    html = get_data(url)
    urls = get_url_lst(html, url)

    for url in urls:
        if url in url_visited:
            continue
        do_crawl(url, depth + 1)

    return url_visited


def get_elem(domain_url, q):
    """
    На входе список пройденных url
    На выходе значения тегов

    """
    global scanned_urls
    conn = engine.connect()

    while not q.empty():

        for item in list(q.queue):

            url = q.get()
            with locker:
                scanned_urls.add(url)

            # if url in do_crawl(domain_url):
            html = get_data(url)
            title = normalize_xpath_result(html.html.xpath('//title/text()'))
            desc = normalize_xpath_result(html.html.xpath('//meta[@name="description"]/@content'))
            h1 = normalize_xpath_result(html.html.xpath('//h1/text()'))
            print(f'{item}: {title}, {desc}, {h1}')
            conn.execute(
                domain.insert().values(title=title,
                                       description=desc,
                                       h1=h1,
                                       url=item,
                                       domain=domain_url),
            )

        conn.close()


def normalize_xpath_result(html_elem):

    """
    На входе html элемент list
    На выходе html элемент str

    """

    if html_elem and len(html_elem) > 0:
        return html_elem[0].strip()
    return ''


def main():
    domain_url = input('Введите домен для анализа: ').strip()
    res = do_crawl(domain_url)
    for url in res:
        q.put(url)
    with ThreadPoolExecutor(max_workers=3) as ex:
        for _ in range(3):
            ex.submit(get_elem, domain_url, q)

    # abc = get_elem(domain_url, res)
    # print(abc)


if __name__ == '__main__':
    main()

    # while True:
    #     if domain_url[:7] == 'http://' or domain_url[:8] == 'https://':
    #         res = do_crawl(domain_url)
    #         abc = get_elem(domain_url, res)
    #         print(abc)
    #     else:
    #         print('Введите протокол домена')

