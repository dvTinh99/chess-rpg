from app.core.database import db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
users_col = db['users']

def get_user(username: str):
    return users_col.find_one({"username": username})

def create_user(username: str, password: str):
    hashed_password = pwd_context.hash(password)
    users_col.insert_one({"username": username, "hashed_password": hashed_password})

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not pwd_context.verify(password, user['hashed_password']):
        return False
    return user
