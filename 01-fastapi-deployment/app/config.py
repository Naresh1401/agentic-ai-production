"""Application configuration loaded from environment variables."""
from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str | None = None
    default_model: str = "gpt-4o-mini"
    app_env: str = "dev"
    log_level: str = "INFO"
    request_timeout_seconds: float = 30.0


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
