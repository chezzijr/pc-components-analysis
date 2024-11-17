from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # postgres_dsn: PostgresDsn
    ignore_insert_components: bool | None = None
    ignore_insert_prices: bool | None = None

    OLLAMA_HOST: str
    OLLAMA_PORT: int
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
