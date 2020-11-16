import time

from selenium import webdriver
from selenium.webdriver.support.select import By
from selenium.common.exceptions import NoSuchElementException
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from src.parsers.post_message import parse_post_message
from src.settings import PATH_DRIVER, chrome_options


class Talkers:

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=PATH_DRIVER, options=chrome_options)
        self.input_name_login = (By.XPATH, '//*[(@name="session[username_or_email]") and not (@type="hidden")]')
        self.input_password_login = (By.XPATH, '//*[(@name="session[password]") and not (@type="hidden")]')
        self.button_login = (By.XPATH, '//*[(@name="session[username_or_email]") and not (@type="hidden")]')
        self.text_box_message = (By.XPATH, "//*[@class='notranslate public-DraftEditor-content']")
        self.button_post_message = (By.XPATH, "//*[(@data-testid='tweetButtonInline') and not (@aria-disabled)]")
        self.alert_success = (By.XPATH, '//*[@role="alert"]')

    async def contain_alert(self):
        teen_seconds = time.time() + 5
        alert = None
        while time.time() <= teen_seconds:
            try:
                alert = self.driver.find_element(*self.alert_success).text
            except NoSuchElementException:
                pass
        return alert

    async def login_twitter(self, username, password):
        url = await parse_post_message()

        try:
            self.driver.get(url)
            self.driver.find_element(*self.input_name_login).send_keys(username)
            self.driver.find_element(*self.input_password_login).send_keys(password)
            self.driver.find_element(*self.button_login).submit()

            alert = await self.contain_alert()

            if alert:
                raise HTTPException(HTTP_400_BAD_REQUEST)

        except HTTPException:
            raise HTTPException(
                HTTP_400_BAD_REQUEST,
                detail=alert
            )
        except Exception as ex:
            raise HTTPException(
                HTTP_400_BAD_REQUEST,
                detail=str(ex)
            )
        return True

    async def post_message(self, username, password, message):
        await self.login_twitter(username, password)
        if len(message) > 280 or len(message) == 0:
            raise HTTPException(
                HTTP_400_BAD_REQUEST,
                detail="Message greater than 280 characters or message contains 0 characters."
            )
        try:
            self.driver.find_element(*self.text_box_message).send_keys(message)

            post_message = True
            while post_message:
                try:
                    self.driver.find_element(*self.button_post_message).click()
                    post_message = False
                except NoSuchElementException:
                    pass

            alert = await self.contain_alert()
            return alert

        except Exception as ex:
            raise HTTPException(
                HTTP_400_BAD_REQUEST,
                detail=str(ex)
            )

    def __del__(self):
        self.driver.close()
        self.driver.quit()
