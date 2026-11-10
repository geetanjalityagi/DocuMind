from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]

UPLOAD_DIR = BASE_DIR / "data" / "uploads"

CHROMA_DIR = BASE_DIR / "data" / "chroma_db"

PROFILES_DIR = BASE_DIR / "data" / "learner_profiles"
PROFILES_DIR.mkdir(parents=True, exist_ok=True)

class Settings(BaseSettings):

    groq_api_key: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore"
    )


settings = Settings()