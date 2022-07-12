from fastapi import Body, FastAPI

app = FastAPI()

# A path operation:  
# Decorator, when its applied to a function, it adds a path to the function, 
#@ clearifies that it is a decorator then reference fastapi reference which is app and send get request
# / is the root path e.g google.com/ is the same as google.com. It could be "/login" meaining url is google.com/login
@app.get("/")
def root(): # The function is called root, async in the beginningoptional i.e you want to talk to the server asyncronously
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}

@app.post("/createposts")
def create_posts(payLoad: dict = Body(...)): # Extracts fields from body and convert to dictionary and store in payLoad
    print(payLoad)
    return {"new_post": f"title {payLoad['title']} content {payLoad['content']}"}