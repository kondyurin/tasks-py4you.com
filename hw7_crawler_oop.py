# Написать парсер на функциях, без использования классов.
# Аналог Скриминг Фрог Сео Спайдера. Вводишь домен, и
# сканер лезет по всем страницам сайта.
# При этом записывает в файл урл, тайтл, дескрипшен, н1.
# И если находит дубль, помечает, что это дубль в файле.

from requests_html import HTMLSession
from time import sleep
from hw7_db import sa, Database


class Crawler:
    def __init__(self):
        self.url_visited = set()
        self.excluded = ['mailto:', 'favicon', '.ico',  # список стоп-слов для урл
                    '.css', '.js', '.jpg',
                    '.jpeg', '.png', '.gif',
                    '#', '?', '.pdf', '.doc', 'tel:']
        self.max_depth = 1
        self.db = Database()

    def get_data(self, url):

        """
        На входе урл, на выходе HTML

        """

        session = HTMLSession()
        data = session.get(url)
        sleep(1)
        return data

    def get_url_lst(self, data, url):

        """
        На входе html, на выходе список ссылок

        """

        links_lst = []
        links = list(set(data.html.xpath('//a/@href')))  # ищем все ссылки и удаляем дубликаты
        for link in links:
            if link and link != url and link not in links_lst and not any(word in link for word in self.excluded):
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

    def do_crawl(self, url, depth=1, max_depth=1):

        """
        На входе url, глубина прохода, макс глубина прохода вглубь
        На выходе список пройденных url

        """
        self.db.create_db()
        self.max_depth = max_depth
        self.url_visited.add(url)  # очередь пройденных url , set

        if depth > self.max_depth:
            return
        html = self.get_data(url)
        urls = self.get_url_lst(html, url)

        for url in urls:
            if url in self.url_visited:
                continue
            self.do_crawl(url, depth + 1)

        return self.url_visited

    def get_elem(self, url, urls_lst):
        item_values = dict{}
        """
        На входе список пройденных url
        На выходе значения тегов

        """
        conn = engine.connect()

        for item in urls_lst:
            html = self.get_data(item)
            title = self.normalize_xpath_result(html.html.xpath('//title/text()'))
            desc = self.normalize_xpath_result(html.html.xpath('//meta[@name="description"]/@content'))
            h1 = self.normalize_xpath_result(html.html.xpath('//h1/text()'))
            print(f'{item}: {title}, {desc}, {h1}')
            item_values = {
                'title':title,
                'description':desc,
                'h1':h1,
                'url':item,
                'domain':url
            }
            query =
            conn.execute(
                # domain.insert().values(title=title,
                #                        description=desc,
                #                        h1=h1,
                #                        url=item,
                #                        domain=url),
            )
        conn.close()

    def normalize_xpath_result(self, html_elem):

        """
        На входе html элемент list
        На выходе html элемент str

        """

        if html_elem and len(html_elem) > 0:
            return html_elem[0].strip()
        return ''


if __name__ == '__main__':
    while True:
        domain_url = input('Введите домен для анализа: ').strip()
        if domain_url[:7] == 'http://' or domain_url[:8] == 'https://':
            res = Crawler().do_crawl(domain_url)
            abc = Crawler().get_elem(domain_url, res)
            print(abc)
        else:
            print('Введите протокол домена')