from fastapi import status,HTTPException,Depends,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import Token
from .. import models,utils
router = APIRouter(tags=['Authentication'])

@router.post("/login",response_model=Token)
def login(user_cred:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Creds")
    if not utils.verify(user_cred.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Creds")
    
    access_token = oauth2.create_acess_token(payload={"userid":user.userid})
    
    return {"access_token":access_token,"token_type":"bearer"}
        
    