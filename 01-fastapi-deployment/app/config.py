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
    max_tokens: int = 1024
    max_retries: int = 2

    # Service auth (off by default for local dev)
    require_auth: bool = False
    api_key: str | None = None

    # Safety
    enable_guardrails: bool = True

    # CORS: comma-separated origins. "*" is convenient for dev; restrict in prod.
    cors_allow_origins: str = "*"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_allow_origins.split(",") if o.strip()]



@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
