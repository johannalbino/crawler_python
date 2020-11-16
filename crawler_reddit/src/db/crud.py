from sqlalchemy.orm import Session
from src.models import SearchReddit
import src.db.schemas as schemas


def insert_posts_reddit(db: Session, search_reddit: schemas.SearchRedditSchemas):
    db_reddit = SearchReddit(
        title=search_reddit.title,
        link=search_reddit.link,
        user_post=search_reddit.user_post
    )
    db.add(db_reddit)
    db.commit()
    db.refresh(db_reddit)
    return db_reddit
