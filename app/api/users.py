# app/api/users.py
from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import get_password_hash, verify_password
from app.db.mongodb import db

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(user_in: UserCreate):
    user = db.users.find_one({"email": user_in.email})
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user_in.password)
    user_data = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed_password
    )
    db.users.insert_one(user_data.dict())
    return user_data
