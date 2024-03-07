from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(prefix="/like", tags=["Like"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def Like(like: schemas.Like, db:Session= Depends(database.get_db), currentUser: int= Depends(oauth2.getCurrentUser)):
    post= db.query(models.Post).filter(models.Post.id==like.post_id).first()
    if not post:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post does not exist")

    like_query= db.query(models.Like).filter(models.Like.post_id == like.post_id, models.Like.user_id == currentUser.id)
    found= like_query.first()

    if (like.dir  == 1):
        if found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="this user has already liked this post")
    
        new_like= models.Like(post_id= like.post_id, user_id=currentUser.id)
        db.add(new_like)
        db.commit()
        return {"message": "Liked"}
    else: 
        if not found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no post with id{like.post_id}")
        
        like_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "liked removed"}
                