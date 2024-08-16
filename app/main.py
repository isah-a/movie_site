from fastapi import FastAPI
from app.api import users, movies, comments, ratings

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(movies.router, prefix="/movies", tags=["Movies"])
app.include_router(comments.router, prefix="/comments", tags=["Comments"])
app.include_router(ratings.router, prefix="/ratings", tags=["Ratings"])
