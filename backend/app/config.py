from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/rentasai"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    app_default_mode: str = "hybrid"
    enable_live_apis: bool = True
    live_api_timeout_seconds: float = 6.0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
