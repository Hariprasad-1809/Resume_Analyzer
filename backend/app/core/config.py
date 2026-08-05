import json
import os
from typing import List, Union, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "development"
    PROJECT_NAME: str = "Resume Role Match Analyzer"
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    ALLOWED_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://resume-analyzer-swart-two.vercel.app",
        "*"
    ]
    MAX_UPLOAD_SIZE: int = 5242880

    openrouter_api_key: Optional[str] = None
    openrouter_model: str = "nvidia/nemotron-3-ultra-550b-a55b:free"
    openrouter_url: str = "https://openrouter.ai/api/v1/chat/completions"

    def get_parsed_origins(self) -> List[str]:
        raw = self.ALLOWED_ORIGINS
        origins = []
        if isinstance(raw, str):
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, list):
                    raw_list = parsed
                else:
                    raw_list = [raw]
            except Exception:
                raw_list = [o.strip() for o in raw.split(",") if o.strip()]
        elif isinstance(raw, list):
            raw_list = raw
        else:
            raw_list = ["*"]

        for item in raw_list:
            cleaned = str(item).strip().rstrip("/")
            if cleaned and cleaned not in origins:
                origins.append(cleaned)

        mandatory = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "https://resume-analyzer-swart-two.vercel.app"
        ]
        for m in mandatory:
            if m not in origins and "*" not in origins:
                origins.append(m)

        return origins

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
