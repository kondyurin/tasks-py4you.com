from requests_html import HTMLSession

session = HTMLSession()

method = 'domain_keywords'

while True:
    try:
        domain_list = '.com'
        domain = input('Введите домен: ')
        if domain_list not in domain:
            raise Exception("incorrect domain name")
    except Exception as e:
        domain = input('enter valid domain name')
    else:
        token = '25bc234aa0bc85faba29358f67bc4400'
        se = 'g_ua'
        page_size = 1

        api_url = f'http://api.serpstat.com/v3/{method}/?query={domain}&token={token}&se={se}'
        response = session.get(api_url)
        data = response.json()

        keys_count = data['result']['total']

        res_dict = {}

        for page in range(1, keys_count + 1):
            api_url = f'http://api.serpstat.com/v3/{method}/?query={domain}&token={token}&se={se}' \
                      f'&page_size={page_size}&page={page}'
            response = session.get(api_url)
            data = response.json()

            for k, v in data['result']['hits'][0].items():
                if k == 'keyword' or k == 'position' or k == 'region_queries_count':
                    print(k, v)
