from datetime import datetime
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


class Post(PostBase): # Response model
    id: int
    created_at: datetime
    
    class Config: # This is a class that is used to configure the Post class to be able to be used in the FastAPI framework
        orm_mode = True 
