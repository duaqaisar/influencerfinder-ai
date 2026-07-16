from pydantic_settings import BaseSettings
from functools import lru_cache

# App configuration class — reads values from environment variables / .env file
class Settings(BaseSettings):
    DATABASE_URL: str            # Database connection string (required, no default)
    DEBUG: bool = True           # Enable/disable debug mode (default: True)
    APP_NAME: str = "Influencer Finder"  # Name of the application
    VERSION: str = "1.0.0"       # Current app version

    class Config:
        env_file = ".env"        # Load environment variables from a .env file
        extra = "ignore"         # Ignore any extra/unknown env vars instead of raising an error

# Cached settings loader — ensures Settings() is only instantiated once (singleton-like behavior)
@lru_cache()
def get_settings():
    return Settings()
