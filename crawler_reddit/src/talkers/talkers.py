from aiohttp import ClientSession
from src.parsers.search_reddit import parser_search_reddit
import bs4


class Talkers:

    def __init__(self):
        self.body_posts = ""

    async def search_reddit(self, text_search):
        url = await parser_search_reddit()

        async with ClientSession() as session:
            async with session.get(f"{url}?q={text_search}&t=week") as resp:
                html = await resp.read()

        page = bs4.BeautifulSoup(html, "html.parser")
        posts = page.find("div", {"class": "rpBJOHq2PR60pnwJlUyP0"})
        breakpoint()
