from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, oauth2, schemas, database
from ..utils import verify_password

router= APIRouter(tags=["authentication"])

@router.post("/login")
async def login(user_creds: OAuth2PasswordRequestForm= Depends(), db: Session= Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_creds.username).first()
    # print(user)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    verify= verify_password(user_creds.password, user.password)

    if not verify:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    #create and return jwt token
    accessToken= oauth2.createAccessToken(data={"userId": user.id})
    return {"accessToken": accessToken, "tokenType": "bearer"}