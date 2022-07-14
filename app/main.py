from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

    
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


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    
    posts = db.query(models.Post).all()

    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model = schemas.Post) 
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)): 
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #                (post.title, post.content, post.published))

    # new_post = cursor.fetchone() # Fetches the returned data from the database
    # conn.commit() # Commits the data to the database
    
    new_post = models.Post(**post.dict()) # **post.dict() unpacks all into a dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # Refreshes the data from the database and updates the object
    
    return new_post # Returns the post


@app.get("/posts/{id}") # Extracts the id from the url, the id is a path parameter
def get_post(id: int,  db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
 
    if not post: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"Post with id {id} not found") # Raises an error if post is not found
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)  # Extracts the id from the url, the id is a path parameter
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (id,))
    # deleted_post = cursor.fetchone() # Fetches the returned data from the database
    # conn.commit() # Commits the data to the database

    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    # cursor.execute("""Update posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
    #                (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} does not exist")
    
    post_query.update(updated_post.dict(), synchronize_session= False)
    db.commit()
    
    return post_query.first()