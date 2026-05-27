from fastapi import APIRouter, HTTPException, Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import settings
from app.services.user_service import get_user, create_user, authenticate_user
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/api/auth/register")
def register(user: UserRegister):
    if get_user(user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    create_user(user.username, user.password)
    return {"msg": "User registered successfully"}

@router.post("/api/auth/token")
def login(user: UserLogin):
    user_obj = authenticate_user(user.username, user.password)
    if not user_obj:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = jwt.encode({
        "sub": user_obj['username'],
        "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    refresh_token = jwt.encode({
        "sub": user_obj['username'],
        "exp": datetime.utcnow() + timedelta(days=30)
    }, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }

@router.get("/api/auth/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user['username']}
