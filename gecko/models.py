import datetime

from sqlmodel import SQLModel, Field


class Coin(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    gecko_id: str | None = Field(index=True, alias="id")
    symbol: str
    name: str


class Price(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    price: float | None = Field(default=None, alias="usd")
    created: datetime.datetime
    coin_id: int | None = Field(default=None, foreign_key="coin.id")
