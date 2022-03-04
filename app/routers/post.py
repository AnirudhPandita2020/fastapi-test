
from .. import models
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import PostCreate, PostOut
from typing import List
from app import oauth2
from sqlalchemy import func

router = APIRouter(tags=['POSTS'])

@router.get("/posts",response_model=List[PostOut])
async def get_posts(db: Session = Depends(get_db),limit:int = 10,skip:int = 0):
    
    
    post_liked_count = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).limit(limit).all()
    
    return post_liked_count


@router.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_posts(post: PostCreate, db: Session = Depends(get_db),get_current_user:int = Depends(oauth2.get_current_user)):
    print(get_current_user)
    new_post = models.Post(**post.dict())
    new_post.userid = get_current_user.userid
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/posts/{id}",response_model=PostOut)
def getpost(id: int, db: Session = Depends(get_db),get_current_user:int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Does not exists")
    
        
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),get_current_user:int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Does not exists")
    
    if post.first().userid != get_current_user.userid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = "Access Denied")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}")
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db),get_current_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    _post = post_query.first()
    if _post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Does not exists")
    
    if _post.userid != get_current_user.userid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = "Access Denied")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()