from requests_html import HTMLSession

session = HTMLSession()

url = ['https://www.dochkisinochki.ru/icatalog/categories/molochnye_smesi/']
keyword = 'молочные смеси'
r = session.get(url[0])

title = r.html.xpath('//title/text()')
desc = r.html.xpath('//meta[@name="description"]/@content')
h1 = r.html.xpath('//h1/text()')

data_lst = [url, title, desc, h1]
character_count = [len(elem[0].replace("  "," ")) for elem in data_lst]  # подсчет кол-ва символов
word_count = [len(elem[0].replace("  "," ").split(' ')) for elem in data_lst]  # подсчет кол-ва слов
keyword_count = [elem[0].count(keyword) for elem in data_lst]  # подсчет кол-ва вхождений
keyword_count_percent = [i/k*100 for i,k in zip(keyword_count, word_count)]  # подсчет плотности
unique_word = [len(set(elem[0].split(' '))) for elem in data_lst]  # подсчет кол-ва уникальных фраз

res_dict = {
      'result': [
            {
                  'url': {
                        'text': url[0],
                        'keyword': keyword,
                        'character_count': character_count[0],
                        'word_count': word_count[0],
                        'title': {
                              'text': title[0],
                              'character_count': character_count[1],
                              'word_count': word_count[1],
                              'keyword_count': keyword_count[1],
                              'keyword_count_percent': keyword_count_percent[1],
                              'unique_word': unique_word[1]
                        },
                        'desc': {
                              'text': desc[0],
                              'character_count': character_count[2],
                              'word_count': word_count[2],
                              'keyword_count': keyword_count[2],
                              'keyword_count_percent': keyword_count_percent[2],
                              'unique_word': unique_word[2]
                        },
                        'h1': {
                              'text': h1[0],
                              'character_count': character_count[3],
                              'word_count': word_count[3],
                              'keyword_count': keyword_count[3],
                              'keyword_count_percent': keyword_count_percent[3],
                              'unique_word': unique_word[3]
                        }
                  }
            }
      ]
}

res_dict = res_dict['result'][0]['url']

pprint('Кол-во символов: url({}),'.format(res_dict.get('character_count')),
      'title({}),'.format(res_dict['title'].get('character_count')),
      'meta description({}),'.format(res_dict['desc'].get('character_count')),
      'h1({})'.format(res_dict['h1'].get('character_count')))
print('Кол-во слов: url({}),'.format(res_dict.get('word_count')),
      'title({}),'.format(res_dict['title'].get('word_count')),
      'meta description({}),'.format(res_dict['desc'].get('word_count')),
      'h1({})'.format(res_dict['h1'].get('word_count')))
print('Кол-во вхождений ключевого слова: title({}),'.format(res_dict['title'].get('keyword_count')),
      'meta description({}),'.format(res_dict['desc'].get('keyword_count')),
      'h1({})'.format(res_dict['h1'].get('keyword_count')))
print('Плотность ключевого слова: title({}%),'.format(round(res_dict['title'].get('keyword_count_percent'), 1)),
      'meta description({}%),'.format(round(res_dict['desc'].get('keyword_count_percent'), 1)),
      'h1({}%)'.format(round(res_dict['h1'].get('keyword_count_percent'), 1)))
print('Кол-во уникальных слов: title({}),'.format(res_dict['title'].get('unique_word')),
      'meta description({}),'.format(res_dict['desc'].get('unique_word')),
      'h1({})'.format(res_dict['h1'].get('unique_word')))