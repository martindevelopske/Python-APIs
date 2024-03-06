from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import List
import os
from ..database import engine, get_db
from sqlalchemy.orm import Session
from .. import models
from .. import schemas
from passlib.context import CryptContext
from .. import oauth2

router=APIRouter(prefix="/posts", tags=["posts"])
@router.get("/", response_model=List[schemas.Postres])
async def get_posts(db:Session= Depends(get_db), currentUser: int=Depends(oauth2.getCurrentUser)):
    posts= db.query(models.Post).filter(models.Post.owner_id == currentUser.id)
    return posts

@router.get("/{id}", response_model=schemas.Postres)
async def get_posts(id: int, res: Response, db:Session= Depends(get_db), currentUser: int=Depends(oauth2.getCurrentUser)):
    post= db.query(models.Post).filter(models.Post.id==id).first()
    if post: 
        return  post
    # res.status_code=status.HTTP_404_NOT_FOUND
    # return {"post": "post not found"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with that ID does not exist")
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Postres)
async def create_post(post: schemas.PostCreate, res:Response, db:Session= Depends(get_db), currentUser: int=Depends(oauth2.getCurrentUser)):
    #title str, content str, category, bool published/draft
    
    post_dict= post.model_dump()
    new_post= models.Post(**post_dict, owner_id=currentUser.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db:Session= Depends(get_db), currentUser: int=Depends(oauth2.getCurrentUser)):
   query= db.query(models.Post).filter(models.Post.id==id)
   
   if query.first() is not None:
       
       if query.first().owner_id != currentUser.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you cannot delete a post that does not belong to you.")
       
       query.delete(synchronize_session=False)
       db.commit()
       return {"message": "post was successfully deleted"}  
   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post does not exist")
       
@router.put("/{id}")
async def update_post(id:int, postdata: schemas.PostCreate, db:Session= Depends(get_db), response_model=schemas.Postres, currentUser: int=Depends(oauth2.getCurrentUser)):
    query=db.query(models.Post).filter(models.Post.id == id)
    post=query.first()
    post_dict= postdata.model_dump()

    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post does not exist.")
    
    if post.owner_id != currentUser.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you cannot updated a post that does not belong to you.")
    query.update(post_dict, synchronize_session=False)
    db.commit()
    
    return query.first()