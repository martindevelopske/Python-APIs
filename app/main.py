from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import os
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import models
from . import schemas
from passlib.context import CryptContext
from .routers import posts, users, auth

models.Base.metadata.create_all(bind=engine)



#init app
app = FastAPI()




my_posts=[{"id": 1, "title": "Nakamoto", "content": "hello from post"}, {"id": 2, "title": "post tetatet", "content": "hello from post"}]




db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')


def get_post_by_id(posts, post_id):
    for post in posts:
        if post["id"] == post_id:
            return post
    return None

def get_index(id):
    for i, post in enumerate(my_posts):
        # print(i, post)
        if post["id"] == id:
            return i


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
@app.get("/")
async def root(db: Session= Depends(get_db)):
    return {"message": "welcome to my api blud!!"}

