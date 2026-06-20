from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="JOBTRACKER_",
        extra="ignore",
    )

    app_name: str = "JobTracker API"
    database_url: str = "postgresql+psycopg://jobtracker:change-me@localhost:5432/jobtracker"
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
