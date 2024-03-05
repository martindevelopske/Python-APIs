from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas



SECRET_KEY="justarandomlongstring"
ALG="HS256"
EXP=30  #mins


def createAccessToken(data: dict):
    to_encode= data.copy()
    expire= datetime.now() + timedelta(minutes=EXP)
    to_encode.update({"exp": expire})

    encoded_token=jwt.encode(to_encode, SECRET_KEY, algorithm=ALG)
    return encoded_token


def verifyAccessToken(token: str, credentialsException):

    try:

        payload=jwt.decode(token, SECRET_KEY, algorithms=ALG)
        id= payload.get("userId")
        if not id:
            raise credentialsException
        
        tokenData=schemas.TokenData(id=id)

    except JWTError:
        raise credentialsException
    
def getCurrentUser:
    