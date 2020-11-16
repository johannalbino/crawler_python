from fastapi import APIRouter
from starlette.responses import JSONResponse
from src.talkers.talkers import Talkers
from src.schemas.twitter import TwitterPost

post_message_router = APIRouter()


@post_message_router.post("/post_message_twitter")
async def post_message(twitter: TwitterPost):
    talker = Talkers()
    message_post = await talker.post_message(twitter.username, twitter.password, twitter.message)

    return JSONResponse({"message": message_post}, status_code=200)
