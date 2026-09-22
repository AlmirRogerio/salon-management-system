from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Salon Management System"
    debug: bool = False

    timezone: str = "America/Sao_Paulo"

    database_url: str = "mysql://salon:salon@db:3306/salon"

    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    admin_name: str = "Leila"
    admin_email: str = "leila@salao.com"
    admin_phone: str = "11999999999"
    admin_password: str = "leila12345"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
