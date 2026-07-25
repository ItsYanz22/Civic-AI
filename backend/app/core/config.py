"""Application settings loaded from the environment.

Plain FastAPI — no database, no secrets required. Everything has a sensible
default so the app boots with zero configuration. Override any field via the
environment or a ``.env`` file.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # --- Project metadata -------------------------------------------------
    PROJECT_NAME: str = "Procura API"
    DESCRIPTION: str = "Plain FastAPI backend."
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"

    # --- Runtime ----------------------------------------------------------
    ENVIRONMENT: Literal["local", "test", "staging", "production"] = "local"
    DEBUG: bool = False
    ENABLE_DOCS: bool = True
    LOG_LEVEL: str = "INFO"
    LOG_JSON: bool = False

    # --- CORS (comma-separated origins) -----------------------------------
    BACKEND_CORS_ORIGINS: str = ""

    @property
    def cors_origins(self) -> list[str]:
        if not self.BACKEND_CORS_ORIGINS:
            return []
        return [o.strip() for o in self.BACKEND_CORS_ORIGINS.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"


@lru_cache
def get_settings() -> Settings:
    """Return the cached settings singleton."""
    return Settings()


settings = get_settings()
