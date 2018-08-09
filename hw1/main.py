from requests_html import HTMLSession
session = HTMLSession()
url = ['https://www.dochkisinochki.ru/icatalog/categories/molochnye_smesi/']
keyword = 'смеси'
r = session.get(url[0])
title = r.html.xpath('//title/text()')
desc = r.html.xpath('//meta[@name="description"]/@content')
h1 = r.html.xpath('//h1/text()')
data_lst = [url, title, desc, h1]
character_count = [len(elem[0].replace("  "," ")) for elem in data_lst] #подсчет кол-ва символов
word_count = [len(elem[0].replace("  "," ").split(' ')) for elem in data_lst] #подсчет кол-ва слов
keyword_count = [elem[0].count(keyword) for elem in data_lst] #подсчет кол-ва вхождений
keyword_count_percent = [i/k*100 for i,k in zip(keyword_count, word_count)] #подсчет плотности
print(f'Кол-во символов: url({character_count[0]}), title({character_count[1]}), meta description({character_count[2]}), h1({character_count[3]})')
print(f'Кол-во слов: url({word_count[0]}), title({word_count[1]}), meta description({word_count[2]}), h1({word_count[3]})')
print(f'Кол-во вхождений ключевого слова {keyword}: title({keyword_count[1]}), meta description({keyword_count[2]}), h1({keyword_count[3]})')
print(f'Плотность ключевого слова {keyword}: title({round(keyword_count_percent[1], 1)}%), meta description({round(keyword_count_percent[2], 1)}%), h1({round(keyword_count_percent[3], 1)}%)')
