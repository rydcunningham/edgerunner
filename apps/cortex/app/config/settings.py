from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Keys
    FIRECRAWL_API_KEY: str
    SUPABASE_KEY: str
    
    # Supabase Configuration
    SUPABASE_URL: str
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 