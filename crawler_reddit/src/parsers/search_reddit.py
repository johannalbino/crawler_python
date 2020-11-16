from aiohttp import ClientSession
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


async def parser_search_reddit():

    async with ClientSession() as session:
        async with session.get("https://www.reddit.com/") as resp:
            status_code = resp.status
    if status_code != 200:
        raise HTTPException(
            HTTP_400_BAD_REQUEST,
            detail="Site is unavailable."
        )

    return "https://www.reddit.com/"
