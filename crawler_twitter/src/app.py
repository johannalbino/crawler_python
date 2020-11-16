from fastapi import FastAPI
import uvicorn
from src.handlers.post_message import post_message_router


app = FastAPI(
    title="Brincando de crawler",
    docs_url="/docs",
    redoc_url="/redocs"
)

app.include_router(post_message_router)


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        debug=True,
        reload=True,
        workers=1
    )
