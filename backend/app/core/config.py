import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    claude_model: str = "claude-3-5-sonnet-20241022"
    gemini_api_key: str = ""
    ai_provider: str = "gemini"
    frontend_origin: str = "http://localhost:5173"
    frontend_url: str = ""
    allowed_origins: str = "http://localhost:3000,http://localhost:5173"
    api_bearer_token: str = "sisa-hackathon-secure-2025"
    require_api_bearer_token: str = "false"
    max_file_size_mb: int = 10
    app_version: str = "1.0.0"
    environment: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()


def get_cors_origins() -> list:
    """
    Returns explicit CORS origins.
    Always allows localhost for local development and optionally
    adds a configured production frontend URL.
    """
    origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    frontend_url = os.getenv("FRONTEND_URL", "").strip().rstrip("/")
    if frontend_url and frontend_url not in origins:
        origins.append(frontend_url)
    return origins


def get_cors_origin_regex() -> str:
    """
    Allow Vercel preview and production subdomains.
    """
    return r"https://.*\.vercel\.app"

