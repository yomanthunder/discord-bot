# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DISCORD_CLIENT_ID: str
    DISCORD_CLIENT_SECRET: str
    DISCORD_REDIRECT_URI:str
    DISCORD_PUBLIC_KEY:str
    DISCORD_BOT_TOKEN:str
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()  # type: ignore
