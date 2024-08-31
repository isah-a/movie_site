from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .routers import users, movies, ratings, comments
from .database import engine, Base
from .auth import get_current_user
from .logging_config import LOGGING_CONFIG
import logging

Base.metadata.create_all(bind=engine)

logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI()

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)

    logger.info(f"Response: {response.status_code} {request.method} {request.url}")

    return response

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
