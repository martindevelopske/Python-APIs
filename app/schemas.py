from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool
    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool

class PostCreate(PostBase):
    pass

class Postres(PostBase):
    id: int
    created_at: datetime

    # class Config:
    #     orm_mode=True

class PostUpdate(PostBase):
    pass

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class Token(BaseModel):
    accessToken: str
    tokenType: str

class TokenData(BaseModel):
    id: Optional[str]= None