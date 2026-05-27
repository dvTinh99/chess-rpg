from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'your-secret-key')
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    MONGO_URI: str = os.getenv('MONGO_URI', 'mongodb://localhost:27017/chessrpg')
    MONGO_DB: str = os.getenv('MONGO_DB', 'chessrpg')

settings = Settings()
