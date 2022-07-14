from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# Class using pydantic to validate our request body
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    
    
while True:
    
    try:
        conn = psycopg2.connect(host = "localhost", database = "fastapi", user = "postgres", password = "password123", cursor_factory=RealDictCursor) # Connect to database
        # cursor_factory is used to return columns as dictionaries
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(3)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id": 2}]

def find_post(id): 
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

# A path operation:  
# Decorator, when its applied to a function, it adds a path to the function, 
#@ clearifies that it is a decorator then reference fastapi reference which is app and send get request
# / is the root path e.g google.com/ is the same as google.com. It could be "/login" meaining url is google.com/login
@app.get("/")
def root(): # The function is called root, async in the beginningoptional i.e you want to talk to the server asyncronously
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()

    return {"data": posts}

# Extract data and send it back
@app.post("/posts", status_code=status.HTTP_201_CREATED) 
def create_posts(post: Post): # Automaticly extracts the data via post
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
                   (post.title, post.content, post.published))
    # %s is a variable that is used to insert data into the database
    # First %s is the title, second %s is the content, third %s is the published
    
    new_post = cursor.fetchone() # Fetches the returned data from the database
    conn.commit() # Commits the data to the database
    return {"data": new_post} # Returns the post

@app.get("/posts/{id}") # Extracts the id from the url, the id is a path parameter
def get_post(id: int): #Fast api will auto extract that id and we can pass it directly to function
    
    post = find_post(int(id)) # Finds the post with the id, manually make it an int
    if not post: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"Post with id {id} not found") # Raises an error if post is not found
    print(post)
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)  # Extracts the id from the url, the id is a path parameter
def delete_post(id: int):
    # deleting post
    # find the index in the array that has required ID 
    # my_posts.pop(index)
    index = find_index_post(id)
    
    if index is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    index = find_index_post(id)
    
    if index is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    post_dict = post.dict() # Converts the post to a dictionary
    post_dict["id"] = id # Adds an id to the post
    my_posts[index] = post_dict 
    return {"data": post_dict} 