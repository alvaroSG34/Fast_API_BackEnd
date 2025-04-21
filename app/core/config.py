from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    DATABASE_URL: str
    FRONTEND_ORIGIN: str
    secret_key: str

    # Stripe
    stripe_secret_key: str
    stripe_publishable_key: str
    stripe_webhook_secret: str | None = None  # si no estás usando webhook aún

    class Config:
        env_file = ".env"

settings = Settings()
