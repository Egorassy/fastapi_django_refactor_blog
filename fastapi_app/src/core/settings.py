from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Blogicum"
    database_url: str

    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "blog"
    postgres_host: str = "postgres"
    postgres_port: int = 5432

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    media_dir: str = "media"
    log_level: str = "INFO"


settings = Settings()
