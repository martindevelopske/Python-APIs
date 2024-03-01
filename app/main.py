from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import os
import psycopg2
from psycopg2.extras import RealDictCursor


app = FastAPI()


my_posts=[{"id": 1, "title": "Nakamoto", "content": "hello from post"}, {"id": 2, "title": "post tetatet", "content": "hello from post"}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')

try:
    # conn= psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password, cursor_factory=RealDictCursor, )
    conn = psycopg2.connect("dbname=fast user=martin port=5432 password=password")
    cursor=conn.cursor()
    print("Database connection successfull")
except Exception as error:
    print("connecting to database failed")
    print(error)

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


@app.get("/")
async def root():
    return {"message": "welcome to my api blud!!"}

@app.get("/posts")
async def get_posts():
    return {"posts": my_posts}

@app.get("/posts/{id}")
async def get_posts(id: int, res: Response):
    print(id)    
    post= get_post_by_id(my_posts, id)
    if post: 
        return {"POST": post}
    # res.status_code=status.HTTP_404_NOT_FOUND
    # return {"post": "post not found"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with that ID does not exist")
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post, res:Response):
    #title str, content str, category, bool published/draft
    
    print(post)
    print(post.model_dump())
    post_dict= post.model_dump()
    post_dict["id"]= randrange(0, 100000)
    my_posts.append(post_dict)
    return {"message": "successfully created", "post": post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
   post= get_post_by_id(my_posts, id)
   if post:
       index =get_index(id)
       my_posts.pop(index)
       return {"message": "post was successfully deleted"}  
   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post does not exist")
       
@app.put("/posts/{id}")
async def update_post(id:int, post: Post):
    oldPostIndex= get_index(id)
    if not oldPostIndex:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post does not exist.")
    post_dict= post.model_dump()
    post_dict["id"]=id
    my_posts[oldPostIndex]= post_dict
    return {"data": post_dict}
