from sqlalchemy import create_engine
from settings import settings
from parts import Base

postgres_dsn = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
engine = create_engine(postgres_dsn)
Base.metadata.create_all(engine)
