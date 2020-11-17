from typing import Dict
from sqlalchemy.orm import Session
from src.models import SearchReddit


def insert_posts_reddit(search_reddit: Dict, db: Session):
    db_reddit = SearchReddit(
        title=search_reddit['title'],
        link=search_reddit['link'],
        user_post=search_reddit['user_post']
    )
    db.add(db_reddit)
    db.commit()
    db.refresh(db_reddit)
    return db_reddit
