from pydantic.main import BaseModel


class SearchRedditSchemas(BaseModel):
    title: str
    link: str
    user_post: str

    class Config:
        arbitrary_types_allowed = True
