# app/routers/movies.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from ..dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)

@router.post("/", response_model=schemas.Movie)
def add_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_movie(db=db, movie=movie, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Movie])
def view_all_movies(db: Session = Depends(get_db)):
    return db.query(models.Movie).all()

@router.get("/{movie_id}", response_model=schemas.Movie)
def view_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = crud.get_movie(db=db, movie_id=movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.put("/{movie_id}", response_model=schemas.Movie)
def edit_movie(movie_id: int, movie: schemas.MovieCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_movie = crud.get_movie(db=db, movie_id=movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    if db_movie.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this movie")
    for key, value in movie.dict().items():
        setattr(db_movie, key, value)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_movie = crud.get_movie(db=db, movie_id=movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    if db_movie.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this movie")
    db.delete(db_movie)
    db.commit()
    return {"message": "Movie deleted successfully"}
