from sqlmodel import SQLModel, Field


class Coin(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    gecko_id: str | None = Field(index=True, alias="id")
    symbol: str
    name: str


class Price: ...
