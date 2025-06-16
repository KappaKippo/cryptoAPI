from gecko.config import settings
from sqlmodel import create_engine

sqlite_url = f"sqlite:///{settings.database_name}.db"
engine = create_engine(sqlite_url, echo=True)
