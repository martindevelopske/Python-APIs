from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import posts, users, auth, likes
from . import models


models.Base.metadata.create_all(bind=engine)


#init app
app = FastAPI()


#cors
origins=["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(likes.router)
@app.get("/")
async def root(db: Session= Depends(get_db)):
    return {"message": "welcome to my api blud!!"}

