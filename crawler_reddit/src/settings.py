from sqlalchemy import create_engine
from src.db.base_class import Base
from sqlalchemy.orm import sessionmaker, Session
from decouple import config


SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI')


class DatabasePSQL:

    @classmethod
    def session_database(cls):
        engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)
        db: Session = session()
        return db
