import time
from fastapi import Depends
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from src.db.database import SessionLocal
from src.parsers.search_reddit import parser_search_reddit
import bs4
from selenium.webdriver import Chrome
from src.settings import PATH_DRIVER, chrome_options
from src.db.crud import insert_posts_reddit


class Talkers:

    def __init__(self):
        self.driver = Chrome(executable_path=PATH_DRIVER, options=chrome_options)
        self.body_posts = (By.CLASS_NAME, "rpBJOHq2PR60pnwJlUyP0")
        self.posts_from = (By.ID, "search-results-time")
        self.posts_from_menu = (By.XPATH, "//*[@role='menu']")
        self.input_text_search = (By.ID, "header-search-bar")

    async def await_element_to_present(self, element, timeout=5):
        min_await = time.time() + timeout
        find_element = False
        while time.time() <= min_await:
            try:
                self.driver.find_element(*element)
                find_element = True
            except NoSuchElementException:
                pass

        return find_element

    async def search_reddit(self, text_search, db: Session):
        url = await parser_search_reddit()
        self.driver.get(url)
        self.driver.find_element(*self.input_text_search).send_keys(text_search)
        self.driver.find_element(*self.input_text_search).submit()
        if await self.await_element_to_present(self.posts_from):
            self.driver.find_element(*self.posts_from).click()
        else:
            raise HTTPException(
                HTTP_400_BAD_REQUEST,
                detail="Ocorreu um erro inesperado."
            )

        options = self.driver.find_element(*self.posts_from_menu).find_elements_by_tag_name('a')
        try:
            [option.click() for option in options if "Week" in option.text]
        except StaleElementReferenceException:
            pass
        response = list()
        if await self.await_element_to_present(self.body_posts):
            page = bs4.BeautifulSoup(self.driver.page_source, "html.parser")
            posts = page.find("div", {"class": "rpBJOHq2PR60pnwJlUyP0"})

            for index, post in enumerate(posts.find_all("div", {"tabindex": "-1"})):
                if index > 14:
                    break

                payload = {
                    "title": post.find('h3').text,
                    "link": f"{url}{posts.find('div', {'tabindex': '-1'}).find('a', {'data-click-id': 'body'}).attrs['href']}",
                    "user_post": post.find('a', {'data-click-id': 'subreddit'}).text
                }

                insert_posts_reddit(search_reddit=payload, db=db)
                response.append(payload)
        return response

    def __del__(self):
        self.driver.close()
        self.driver.quit()
