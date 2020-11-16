from fastapi import FastAPI
import uvicorn
from fastapi_sqlalchemy import DBSessionMiddleware
from src.handlers.search_reddit import search_reddit_router
from src.settings import SQLALCHEMY_DATABASE_URI

app = FastAPI(
    title="Brincando de crawler - REDDIT",
    docs_url="/docs",
    redoc_url="/redocs"
)

app.include_router(search_reddit_router)
app.add_middleware(DBSessionMiddleware, db_url=SQLALCHEMY_DATABASE_URI)


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        debug=True,
        reload=True,
        workers=1
    )
