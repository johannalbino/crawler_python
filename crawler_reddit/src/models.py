from sqlalchemy import Column, String, Integer
from src.db.base_class import Base
from src.settings import DatabasePSQL

db = DatabasePSQL.session_database()


class SearchReddit(Base):
    __tablename__ = 'search_reddit'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    link = Column(String)
    user_post = Column(String)

    class Config:
        arbitrary_types_allowed = True