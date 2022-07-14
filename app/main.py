from random import randrange
from turtle import pos
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Class using pydantic to validate our request body
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    
    
while True:
    
    try:
        conn = psycopg2.connect(host = "localhost", database = "fastapi", user = "postgres", 
                                password = "password123", cursor_factory=RealDictCursor) # Connect to database
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


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all() # Query all posts from the database
    
    return {"data": posts}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()

    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED) 
def create_posts(post: Post): 
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
                   (post.title, post.content, post.published))

    new_post = cursor.fetchone() # Fetches the returned data from the database
    conn.commit() # Commits the data to the database
    
    return {"data": new_post} # Returns the post


@app.get("/posts/{id}") # Extracts the id from the url, the id is a path parameter
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    post = cursor.fetchone()    
 
    if not post: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"Post with id {id} not found") # Raises an error if post is not found
    print(post)
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)  # Extracts the id from the url, the id is a path parameter
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (id,))
    deleted_post = cursor.fetchone() # Fetches the returned data from the database
    conn.commit() # Commits the data to the database
        
    if deleted_post is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} does not exist")
        
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    cursor.execute("""Update posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
                   (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()
    
    if updated_post is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    return {"data": updated_post} 