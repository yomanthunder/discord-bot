# app/core/config.py
from pydantic_settings import BaseSettings

from dotenv import load_dotenv
load_dotenv()
class Settings(BaseSettings):
    DISCORD_CLIENT_ID: str
    DISCORD_CLIENT_SECRET: str
    DISCORD_REDIRECT_URI: str
    DISCORD_PUBLIC_KEY: str
    DISCORD_BOT_TOKEN: str
    DISCORD_API_VERSION: str = "v10"
    DISCORD_API_BASE_URL: str = "https://discord.com/api/v10"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()  # type: ignore
