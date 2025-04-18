from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    FRONTEND_ORIGIN: str
    secret_key: str

    class Config:
        env_file = ".env"

settings = Settings()
