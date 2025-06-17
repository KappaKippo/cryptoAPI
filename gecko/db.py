from gecko.config import settings
from sqlmodel import create_engine, Session, SQLModel

sqlite_url = f"sqlite:///{settings.database_name}.db"
engine = create_engine(sqlite_url, echo=True)


def create_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
