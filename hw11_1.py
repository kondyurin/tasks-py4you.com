# Написать асинхронный парсер работающий в 100 потоков,
# записывающий данные в базу.
# Аналог Screeming Frog SEO Spider, сохраняющий в базу url,
# title, description, h1, link_level, in_links_count, out_links_count.

import aiohttp
import asyncio
from lxml import html
from hw11_1_db import domain, engine
from concurrent.futures import ThreadPoolExecutor


url = 'https://www.detmir.ru/'
scaned_urls = set()

executor = ThreadPoolExecutor(max_workers=10)


async def worker(q):
    depth = 0
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        while q.qsize() > 0:
            u = await q.get()
            try:
                async with session.get(u) as response:
                    code = await response.text()
                tree = await loop.run_in_executor(executor, html.fromstring, code)

                tree.make_links_absolute(url)
                links = tree.xpath('//a/@href')
                links = set(links)
                conn = engine.connect()
                title = tree.xpath('//title/text()')[0].strip()
                description = tree.xpath('//meta[@name="description"]/@content')[0].strip()
                h1 = tree.xpath('//h1/text()')[0].strip()
                print(u, title, description, h1)

                for link in links:
                    if not link.startswith(url):
                        continue
                    elif link in scaned_urls:
                        continue
                    else:
                        scaned_urls.add(link)
                        await q.put(link)
                    
                conn.execute(
                    domain.insert().values(title=title,
                                           description=description,
                                           h1=h1,
                                           url=u,
                                           domain=url,
                                           link_level=depth),
                )

            except Exception as e:
                print(type(e), e)
            conn.close()


async def main():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        response = await session.get(url)
        code = await response.text()
    tree = html.fromstring(code)
    tree.make_links_absolute(url)
    links = tree.xpath('//a/@href')
    links = set(links)
    qu = asyncio.Queue()
    for link in links:
        if link.startswith(url):
            scaned_urls.add(link)
            await qu.put(link)
    print(qu.qsize())
    tasks = []
    for _ in range(100):
        task = asyncio.Task(worker(qu))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())