from sqlmodel import SQLModel, Field


class Coin(SQLModel, table=True):
    id: str = Field(primary_key=True, alias="id")
    symbol: str = Field()
    name: str = Field()
