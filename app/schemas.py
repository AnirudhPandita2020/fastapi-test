
from datetime import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr, conint

from app.models import User


class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    
class PostCreate(PostBase):
    pass
    

class UserOut(BaseModel):
    userid:int
    email:EmailStr
    created_at:datetime

    class Config:
        orm_mode = True
        
 
class PostResponse(BaseModel):
    id:int
    title:str
    content:str
    published:bool
    user: UserOut
    
    class Config:
        orm_mode = True
    
    
class UserCreate(BaseModel):
    email:EmailStr
    password:str
    

class Userlogin(BaseModel):
    email:EmailStr
    password:str
    
    
class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    id:Optional[str] = None


class Vote(BaseModel):
    post_id:int
    dir:conint(le=1,ge=0)
    
class PostOut(BaseModel):
    Post:PostResponse
    votes:int
    
    class Config:
        orm_mode =True
    
