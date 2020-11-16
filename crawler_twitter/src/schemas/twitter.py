from pydantic import BaseModel


class TwitterPost(BaseModel):
    username: str
    password: str
    message: str
