from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional

############################ USER ##############################################        
        
class UserCreate(BaseModel): # Response model
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
        
    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str

########################## POST ##########################

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


class Post(PostBase): # Response model
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    
    class Config: # This is a class that is used to configure the Post class to be able to be used in the FastAPI framework
        orm_mode = True 
        
    
############################ TOKEN ##############################################

class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    id: Optional[str] = None


######################### VOTE ##############################################

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
    
    # class Config:
    #     orm_mode = True