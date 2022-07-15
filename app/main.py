from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router) # Include the router from the post.py file
app.include_router(user.router) # Include the router from the user.py file
app.include_router(auth.router) # Include the router from the auth.py file

@app.get("/")
def root():
    return {"message": "Hello World"}




