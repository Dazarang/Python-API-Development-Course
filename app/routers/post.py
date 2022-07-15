from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/posts", response_model = List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    
    posts = db.query(models.Post).all()

    return posts


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model = schemas.Post) 
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


@router.get("/posts/{id}", response_model= schemas.Post) # Extracts the id from the url, the id is a path parameter
def get_post(id: int,  db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
 
    if not post: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"Post with id {id} not found") # Raises an error if post is not found
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)  # Extracts the id from the url, the id is a path parameter
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


@router.put("/posts/{id}", response_model = schemas.Post)
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