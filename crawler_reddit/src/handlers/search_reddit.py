from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.database import SessionLocal
from src.schemas.reddit import SearchRedditInput
from src.talkers.talkers import Talkers

search_reddit_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@search_reddit_router.post("/search_reddit")
async def search_reddit(text_search: SearchRedditInput, db: Session = Depends(get_db)):
    talker = Talkers()
    resp = await talker.search_reddit(text_search.text_search)
    pass
