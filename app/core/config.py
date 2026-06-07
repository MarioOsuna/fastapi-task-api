from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Task API"
    database_url: str = "sqlite:///./tasks.db"
    secret_key: str = "change-me-in-production-use-secrets-generate"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 1 day

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
