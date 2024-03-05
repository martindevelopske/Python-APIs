from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import os
from ..database import engine, get_db
from sqlalchemy.orm import Session
from .. import models
from .. import schemas
from ..utils import get_password_hash

router=APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def createUser( user: schemas.UserCreate, db:Session=Depends(get_db)):
    user_dict= user.model_dump()
    user_dict['password']=get_password_hash(user_dict["password"])
    print(user_dict['password'])
    new_user= models.User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
async def getUser(id: int, db: Session= Depends(get_db)):
    user= db.query(models.User).filter(models.User.id== id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" user with id:{id} does not exist")
    
    return user