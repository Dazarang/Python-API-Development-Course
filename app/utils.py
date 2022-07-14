from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # This is a class that is used to hash passwords, bcrypt is a hashing algorithm

def hash(password: str):
    return pwd_context.hash(password)