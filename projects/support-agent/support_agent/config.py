"""Configuration for the capstone support agent."""
from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str | None = None
    small_model: str = "gpt-4o-mini"
    large_model: str = "gpt-4o"
    max_tokens: int = 512
    enable_guardrails: bool = True
    cache_ttl_seconds: float = 300.0
    cors_allow_origins: str = "*"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_allow_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
