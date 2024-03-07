from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, models, database
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings


SECRET_KEY=settings.secret_key
ALG=settings.alg
EXP=settings.exp  #mins

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="login")

def createAccessToken(data: dict):
    to_encode= data.copy()
    expire= datetime.utcnow() + timedelta(minutes=EXP)
    to_encode.update({"exp": expire})

    encoded_token=jwt.encode(to_encode, SECRET_KEY, algorithm=ALG)
    return encoded_token


def verifyAccessToken(token: str, credentialsException):

    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALG])
        id= payload.get("userId")
        if not id:
            raise credentialsException
        
        tokenData=schemas.TokenData(id=id)
        return tokenData
    except JWTError:
        raise credentialsException
    
def getCurrentUser(token: str= Depends(oauth2_scheme), db: Session= Depends(database.get_db)):
    credentialsException= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verifyAccessToken(token, credentialsException)
    user= db.query(models.User).filter(models.User.id == token.id).first()
    return user
    