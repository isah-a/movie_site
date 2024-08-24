from pydantic import BaseModel
from typing import List, Optional

# User Schemas
class UserBase(BaseModel):
    username: str
    email: str
    country: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    movies: List['Movie'] = []

    class Config:
        from_attributes = True

# Movie Schemas
class MovieBase(BaseModel):
    title: str
    description: str

class MovieCreate(MovieBase):
    pass

class MovieUpdate(MovieBase):
    title: Optional[str] = None
    description: Optional[str] = None

class Movie(MovieBase):
    id: int
    owner_id: int
    ratings: List['Rating'] = []
    comments: List['Comment'] = []

    class Config:
        from_attributes = True

# Rating Schemas
class RatingBase(BaseModel):
    score: int

class RatingCreate(RatingBase):
    pass

class Rating(RatingBase):
    id: int
    movie_id: int

    class Config:
        from_attributes = True

# Comment Schemas
class CommentBase(BaseModel):
    content: str
    parent_id: Optional[int]

class CommentCreate(CommentBase):
    pass

class CommentUpdate(CommentBase):
    content: Optional[str] = None
    parent_id: Optional[int] = None

class Comment(CommentBase):
    id: int
    movie_id: int
    owner_id: int
    replies: List['Comment'] = []

    class Config:
        from_attributes = True

# Token Schema
class TokenData(BaseModel):
    username: Optional[str] = None
