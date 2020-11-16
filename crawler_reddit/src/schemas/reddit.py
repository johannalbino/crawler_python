from pydantic import BaseModel


class SearchRedditInput(BaseModel):
    text_search: str
