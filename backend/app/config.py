"""Application configuration module.

Loads all settings from environment variables (via a .env file) using
pydantic-settings. Provides a single `settings` object that is imported
throughout the application.

All secrets (SECRET_KEY, KINOPOISK_API_KEY, DATABASE_URL) must be
defined in the .env file and must never be committed to Git.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        DATABASE_URL: SQLAlchemy connection string for PostgreSQL.
        SECRET_KEY: Secret key used to sign JWT tokens.
        ALGORITHM: JWT signing algorithm (default: HS256).
        ACCESS_TOKEN_EXPIRE_MINUTES: Token lifetime in minutes.
        KINOPOISK_API_KEY: API key for kinopoiskapiunofficial.tech.
        KINOPOISK_BASE_URL: Base URL for the Kinopoisk API.
        DEBUG: Enables debug mode (verbose SQL logging, etc.).
    """

    DATABASE_URL: str = (
        "postgresql+psycopg2://tvfriend:tvfriend@localhost:5432/tvfriend"
    )
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    KINOPOISK_API_KEY: str = ""
    KINOPOISK_BASE_URL: str = "https://kinopoiskapiunofficial.tech"
    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()