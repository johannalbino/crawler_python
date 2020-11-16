import os
import sys
from selenium import webdriver

PLATFORM = f"{sys.platform}/chromedriver.exe" if sys.platform == "win32" else f"{sys.platform}/chromedriver"
PATH_DRIVER = os.path.join(os.path.dirname(__file__), f"media/{PLATFORM}")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

