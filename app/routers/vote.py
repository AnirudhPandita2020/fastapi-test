from fastapi import APIRouter, Depends,status,HTTPException
from sqlalchemy.orm import Session
from .. import schemas,database,models,oauth2
router = APIRouter(tags=["Vote"])

@router.post("/vote",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db :Session =Depends(database.get_db),get_current_user:int= Depends(oauth2.get_current_user)):
    
    find_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if find_post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,"Does not exists")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == get_current_user.userid)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail = "Already Liked")
        
        new_vote =models.Vote(post_id = vote.post_id,user_id = get_current_user.userid)
        db.add(new_vote)
        db.commit()
        return {"message":"Liked the Post"}
        
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        
        return {"message":"Unliked the Post"}