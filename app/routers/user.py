from .. import models,utils
from fastapi import status,HTTPException,Depends,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import UserCreate,UserOut


router = APIRouter(tags=["USER"])

@router.post("/users",status_code=status.HTTP_201_CREATED,response_model=UserOut)
def create_user(user:UserCreate,db:Session = Depends(get_db)):
    
    exits_user = db.query(models.User).filter(models.User.email == user.email).first()
    if exits_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User Exists Already")
    hased_pass = utils.hash(user.password)
    user.password = hased_pass
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
@router.get("/users/{id}",response_model=UserOut)
def get_user(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.userid == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Does not exists")
    return user