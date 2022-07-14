from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'postgreeql://<username>:<password>@<ip-adress/hostname>/<database-name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL) # echo is used to print the query

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # SessionLocal is a class that is used to create a session

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()