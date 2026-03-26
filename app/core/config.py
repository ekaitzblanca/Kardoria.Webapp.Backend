from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    CHARACTER_TABLE_NAME: str = "charapters"

    class Config:
        env_file = ".env"

settings = Settings()