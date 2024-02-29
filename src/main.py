from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "welcome to my api blud!!"}

@app.get("/posts")
async def get_posts():
    return {"data": "this is your post"}

@app.post("/posts")
async def create_post(body: dict= Body(...)):
    #title str, content str
    
    print(body)
    return {"message": "successfully created", "post": body}