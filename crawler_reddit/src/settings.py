from sqlalchemy import create_engine
from src.db.base_class import Base
from sqlalchemy.orm import sessionmaker, Session
from decouple import config
import os
import sys
from selenium import webdriver

PLATFORM = f"{sys.platform}/chromedriver.exe" if sys.platform == "win32" else f"{sys.platform}/chromedriver"
PATH_DRIVER = os.path.join(os.path.dirname(__file__), f"media/{PLATFORM}")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-notifications")


SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI')


class DatabasePSQL:

    @classmethod
    def session_database(cls):
        engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)
        db: Session = session()
        return db
