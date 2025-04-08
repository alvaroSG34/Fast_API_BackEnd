from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    FRONTEND_ORIGIN: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
