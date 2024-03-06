from fastapi import FastAPI, Depends
import os
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import posts, users, auth
from . import models

models.Base.metadata.create_all(bind=engine)

#init app
app = FastAPI()

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
@app.get("/")
async def root(db: Session= Depends(get_db)):
    return {"message": "welcome to my api blud!!"}

