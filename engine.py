from sqlalchemy import create_engine
from settings import settings
from parts import Base

engine = create_engine(str(settings.postgres_dsn))
Base.metadata.create_all(engine)
