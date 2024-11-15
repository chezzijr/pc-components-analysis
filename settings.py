from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    postgres_dsn: PostgresDsn
    ignore_insert_components: bool | None = None
    ignore_insert_prices: bool | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
