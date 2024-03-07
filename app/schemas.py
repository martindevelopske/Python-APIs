from pydantic import BaseModel, EmailStr, Field
from pydantic.types import conint
from datetime import datetime
from typing import Optional



class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config: 
        orm_mode=True


class Post(BaseModel):
    title: str
    content: str
    created_at: datetime
    id: int
    published: bool
    owner_id: int
   
    class Config:
        orm_mode= True
    # rating: Optional[int] = None

# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

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
    owner_id: int
    owner: UserOut


    # class Config:
    #     orm_mode=True

class PostUpdate(PostBase):
    pass


class Token(BaseModel):
    accessToken: str
    tokenType: str

class TokenData(BaseModel):
    id: Optional[int]= None

class Like(BaseModel):
    post_id: int
    dir: int= Field(..., ge=0, le=1)

class JoinedPostRes(Post):
    post: Post
    likes: int

    class Config:
        orm_mode= True