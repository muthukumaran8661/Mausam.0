"""Application configuration settings."""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Mausam"
    environment: str = "development"
    debug: bool = True
    # Render injects PORT automatically; fall back to 8000 locally
    port: int = int(os.environ.get("PORT", 8000))
    database_url: str = "sqlite:///./mausam.db"
    weather_cache_ttl: int = 600  # 10 minutes in seconds
    cors_origins: str = "*"
    rate_limit_per_minute: int = 120

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def cors_origin_list(self) -> list[str]:
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        return self.environment.lower() in ("production", "prod")


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
