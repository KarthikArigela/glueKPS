from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE, override=True)

class Settings(BaseSettings):
    APP_NAME: str = "GlueKPS-backend"
    ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    
    SUPABASE_DB_URL: str

    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "deepseek/deepseek-v4-flash"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE if ENV_FILE.exists() else None,
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()