from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    postgres_dsn: PostgresDsn
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
