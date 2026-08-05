import os
from typing import List, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "development"
    PROJECT_NAME: str = "Resume Role Match Analyzer"
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    MAX_UPLOAD_SIZE: int = 5242880

    openrouter_api_key: Optional[str] = None
    openrouter_model: str = "nvidia/nemotron-3-ultra-550b-a55b:free"
    openrouter_url: str = "https://openrouter.ai/api/v1/chat/completions"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
