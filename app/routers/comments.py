# app/routers/comments.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from ..dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)

@router.post("/", response_model=schemas.Comment)
def add_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_comment(db=db, comment=comment, user_id=current_user.id)

@router.get("/{movie_id}", response_model=List[schemas.Comment])
def view_comments_for_movie(movie_id: int, db: Session = Depends(get_db)):
    return db.query(models.Comment).filter(models.Comment.movie_id == movie_id).all()
