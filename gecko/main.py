from datetime import datetime

from fastapi import FastAPI, Query, status, Depends
from contextlib import asynccontextmanager
from typing import Annotated

from sqlalchemy import text
from sqlmodel import SQLModel
from starlette.background import BackgroundTasks

from gecko.crud import create_or_update
from gecko.dependencies import get_session
from gecko.db import engine
from gecko.requests import RequestClient
from gecko.models import Coin


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    with engine.connect() as connection:
        connection.execute(text("PRAGMA foreign_keys=ON"))
    yield


app = FastAPI(lifespan=lifespan, title="CoinGecko API")
request_client = RequestClient()


@app.get(
    "/coins_list",
    status_code=status.HTTP_200_OK,
    response_model=list,
    description="This endpoint allows you to query all the supported coins on CoinGecko with coins ID, name and symbol",
)
async def get_coins(
    background_task: BackgroundTasks,
    coin_id: Annotated[str | None, Query(description="Coin ID")] = None,
    symbol: Annotated[str | None, Query(description="Coin symbol")] = None,
    name: Annotated[str | None, Query(description="Coin name")] = None,
    # include_platform: Annotated[bool, Query(description="Include platform and token's contract addresses")] = False,
    # platforms - coin asset platform and contract address - platforms.{key}: string,
    session=Depends(get_session),
):
    params = {"id": coin_id, "symbol": symbol, "name": name}
    response = await request_client.get(url="/coins/list", params=params)
    data = [Coin.model_validate(coin) for coin in response]
    background_task.add_task(create_or_update, session, data)
    return response[:100]


@app.get("/{id}/market_chart")
async def prices(
    coin_id: str,
    days: str,
    vs_currency: str = "usd",
    interval: str = "daily",
    precision: str = 2,
):
    url = f"/coins/{coin_id}/market_chart"
    params = {"days": days, "vs_currency": vs_currency}
    response = await request_client.get(url, params=params)
    all_prices = []
    for price in response["prices"]:
        all_prices.append([datetime.fromtimestamp(price[0] / 1000), price[1]])

    all_prices.remove(all_prices[-1])
    coin_prices = [price_list[-1] for price_list in all_prices]

    window = int(days)
    sma = []
    for i in range(len(coin_prices) - window + 1):
        window_data = coin_prices[i : i + window]
        sma.append(sum(window_data) / window)

    print(sma)
    return all_prices
