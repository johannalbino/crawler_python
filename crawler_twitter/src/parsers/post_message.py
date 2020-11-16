from aiohttp import ClientSession
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


async def parse_post_message():
    async with ClientSession() as session:
        async with session.get("http://twitter.com/login") as resp:
            status_code = resp.status

    if status_code != 200:
        raise HTTPException(
            HTTP_400_BAD_REQUEST,
            detail="Site is unavailable."
        )
    return "http://twitter.com/login"
