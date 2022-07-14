from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

# Class using pydantic to validate our request body
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id": 2}]

# A path operation:  
# Decorator, when its applied to a function, it adds a path to the function, 
#@ clearifies that it is a decorator then reference fastapi reference which is app and send get request
# / is the root path e.g google.com/ is the same as google.com. It could be "/login" meaining url is google.com/login
@app.get("/")
def root(): # The function is called root, async in the beginningoptional i.e you want to talk to the server asyncronously
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# Extract data and send it back
@app.post("/posts")
def create_posts(post: Post): # Automaticly extracts the data via post
    
    my_posts.append(post.dict())
    return {"data": post}

