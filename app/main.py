from fastapi import FastAPI
from .routers import users, movies, ratings, comments
from .database import engine, Base
from .auth import get_current_user
from .logging_config import LOGGING_CONFIG
import logging

Base.metadata.create_all(bind=engine)

logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI()

logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown")

app.include_router(users.router)
app.include_router(movies.router)
app.include_router(ratings.router)
app.include_router(comments.router)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)