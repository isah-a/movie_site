# app/routers/ratings.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from ..dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/ratings",
    tags=["ratings"],
)

@router.post("/", response_model=schemas.Rating)
def rate_movie(rating: schemas.RatingCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_rating(db=db, rating=rating, user_id=current_user.id)

@router.get("/{movie_id}", response_model=List[schemas.Rating])
def get_ratings_for_movie(movie_id: int, db: Session = Depends(get_db)):
    return db.query(models.Rating).filter(models.Rating.movie_id == movie_id).all()
