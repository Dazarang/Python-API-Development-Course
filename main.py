from random import randrange
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

def find_post(id): 
    for p in my_posts:
        if p["id"] == id:
            return p

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
    post_dict = post.dict() # Converts the post to a dictionary
    post_dict["id"] = randrange(0, 1000000) # Adds an id to the post
    my_posts.append(post_dict) # Adds the post to the list
    
    return {"data": post_dict} # Returns the post

@app.get("/posts/{id}") # Extracts the id from the url, the id is a path parameter
def get_post(id: int): #Fast api will auto extract that id and we can pass it directly to function
    
    post = find_post(int(id)) # Finds the post with the id, manually make it an int
    print(post)
    return {"post_detail": post}
 