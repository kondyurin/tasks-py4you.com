# Написать функцию которая на вход принимает ключевое слово и название домена.
# А на выходе возвращает позицию домена по этому слову.
#
# Программа должна работать так:
# Запрашивает ввод домена, запрашивает ввод ключевого слова.
# Выполняет запрос в Гугл, определяет позицию, печатает результат и опять запрашивает домен.
# Пока не введем слово exit. Если произошла ошибка, не ломается и работает дальше.

from requests_html import HTMLSession

while True:
    keyword = input('Введите ключевое слово или exit для выхода: ')
    if keyword == 'exit':
        break
    domain = input('Введите название домена: ')


    def get_domain_position(keyword, domain):
        session = HTMLSession()
        resp = session.get(f'https://www.google.com/search?q={keyword}&num=10&hl=en')
        links = resp.html.xpath('//*[@id="rso"]/div[1]/div/div/div/div/h3/a/@href')
        domains = [x.split('/')[2].replace('www.', '') for x in links if 'http' in x]
        res_list = list(enumerate(domains, start=1))
        for item in res_list:
            if domain in item:
                return item[0]


    a = get_domain_position(keyword, domain.replace('www.', ''))
    print(f'Позиция по ключевому слову \"{keyword}\" домена {domain}: {a}')

