# Полезть в документацию Серпстата, разобраться с тем как формировать запросы на другие методы
# Создать 3 отдельные функции, которые выполняют разные запросы в Serpstat на твое усмотрение.
# Результат печатаем в консоль.

from requests_html import HTMLSession

while True:
    url = input('Введите url страницы или exit для выхода: ')
    if url == 'exit':
        break


    def get_json_data(url, payload):

        """
        Функция делает запрос к API Serpstat и возвращает JSON

        """

        session = HTMLSession()
        resp = session.get(url, params=payload)
        data = resp.json()
        return data


    def get_url_competitors(url):

        """
        Функция возвращает url конкурентов для заданного url.

        """

        url_competitors = []
        url_api = 'http://api.serpstat.com/v3/url_competitors/'
        payload = {'query': url,
                   'token': 'f0a9d28ab759a66858d08f95533f62cf',
                   'se': 'y_213',
                   'page_size': 3,
                   'page': 1}
        for item in get_json_data(url_api, payload)['result']['hits']:
            url_competitors.append(item['url'])
        return url_competitors


    def get_url_keywords():

        """
        Функция возвращает ключевые фразы в топе поисковой системы по URL из get_url_competitors(url).

        """

        url_keywords = []
        url_api = 'http://api.serpstat.com/v3/url_keywords/'
        for link in get_url_competitors(url):
            payload = {'query': link,
                       'token': 'f0a9d28ab759a66858d08f95533f62cf',
                       'se': 'y_213',
                       'page_size': 3,
                       'page': 1}
            for item in get_json_data(url_api, payload)['result']['hits']:
                url_keywords.append(item['keyword'])
        return url_keywords


    def get_related_keywords():

        """
        Функция возвращает похожие запросы для запросов из get_url_keywords().

        """

        related_keywords = []
        url_api = 'http://api.serpstat.com/v3/related_keywords/'
        for keyword in get_url_keywords():
            payload = {'query': keyword,
                       'token': 'f0a9d28ab759a66858d08f95533f62cf',
                       'se': 'y_213',
                       'page_size': 3,
                       'page': 1}
            for item in get_json_data(url_api, payload)['result']['hits']:
                related_keywords.append(item['keyword'])
            return related_keywords


    try:
        print(f'\nДанные для URL {url}:\n')
        print('Похожие URL конкурентов:')
        for link in get_url_competitors(url):
            print(f'{link}')
        print('\nКлючевые фразы для похожих URL конкурентов:')
        for item in get_url_keywords():
            print(f'{item}')
        print('\nПохожие ключевые фразы ключевых фраз конкурентов:')
        for rel_keyword in get_related_keywords():
            print(f'{rel_keyword}')
    except Exception as e:
        print(e)