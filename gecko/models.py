from sqlmodel import SQLModel, Field


class Coin(SQLModel, table=True):
    id: str | None = Field(primary_key=True)
    symbol: str
    name: str
