from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    username: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
