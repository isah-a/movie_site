from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext
from typing import List, Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Users
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Movies
def get_movies(db: Session, skip: int = 0, limit: int = 10) -> List[models.Movie]:
    return db.query(models.Movie).offset(skip).limit(limit).all()

def create_movie(db: Session, movie: schemas.MovieCreate, user_id: int):
    db_movie = models.Movie(**movie.dict(), owner_id=user_id)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def get_movie(db: Session, movie_id: int) -> Optional[models.Movie]:
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

def update_movie(db: Session, movie_id: int, movie_update: schemas.MovieUpdate):
    db_movie = get_movie(db, movie_id)
    if db_movie:
        for key, value in movie_update.dict(exclude_unset=True).items():
            setattr(db_movie, key, value)
        db.commit()
        db.refresh(db_movie)
    return db_movie

def delete_movie(db: Session, movie_id: int):
    db_movie = get_movie(db, movie_id)
    if db_movie:
        db.delete(db_movie)
        db.commit()
    return db_movie

# Ratings
def get_movie_ratings(db: Session, movie_id: int, skip: int = 0, limit: int = 10) -> List[models.Rating]:
    return db.query(models.Rating).filter(models.Rating.movie_id == movie_id).offset(skip).limit(limit).all()

def create_rating(db: Session, rating: schemas.RatingCreate, user_id: int, movie_id: int):
    db_rating = models.Rating(**rating.dict(), owner_id=user_id, movie_id=movie_id)
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def get_rating(db: Session, rating_id: int) -> Optional[models.Rating]:
    return db.query(models.Rating).filter(models.Rating.id == rating_id).first()

def delete_rating(db: Session, rating_id: int):
    db_rating = get_rating(db, rating_id)
    if db_rating:
        db.delete(db_rating)
        db.commit()
    return db_rating

# Comments
def get_movie_comments(db: Session, movie_id: int, skip: int = 0, limit: int = 10) -> List[models.Comment]:
    return db.query(models.Comment).filter(models.Comment.movie_id == movie_id).offset(skip).limit(limit).all()

def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int, movie_id: int, parent_comment_id: Optional[int] = None):
    db_comment = models.Comment(**comment.dict(), owner_id=user_id, movie_id=movie_id, parent_comment_id=parent_comment_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comment(db: Session, comment_id: int) -> Optional[models.Comment]:
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

def update_comment(db: Session, comment_id: int, comment_update: schemas.CommentUpdate):
    db_comment = get_comment(db, comment_id)
    if db_comment:
        for key, value in comment_update.dict(exclude_unset=True).items():
            setattr(db_comment, key, value)
        db.commit()
        db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int):
    db_comment = get_comment(db, comment_id)
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment
