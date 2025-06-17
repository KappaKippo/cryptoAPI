from typing import Annotated

from gecko.client import RequestsClient
from gecko.config import settings
from fastapi import FastAPI, BackgroundTasks, Depends, status, Query
from contextlib import asynccontextmanager
from gecko.storage_interface import StorageManager
from gecko.db import create_tables
from gecko.models import Coin
from gecko.db import get_session
from gecko.utils import get_url
from sqlmodel import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/ping", status_code=status.HTTP_200_OK, response_model=dict)
async def ping():
    ping_url = settings.api_url + "ping"
    client = RequestsClient(url=ping_url)
    response = client.get()

    return response


@app.get("/coins_list", status_code=status.HTTP_201_CREATED, response_model=list[Coin])
async def get_coins(
    background_task: BackgroundTasks, session: Session = Depends(get_session)
):
    coins_list_url = settings.api_url + "coins/list"
    client = RequestsClient(url=coins_list_url)
    response = client.get()

    storage = StorageManager(session)
    for coin in response:
        background_task.add_task(storage.create_objects, Coin(**coin))

    background_task.add_task(storage.commit_and_close)

    return response


@app.get("/coin_price")
async def get_coin_price(
    ids: Annotated[str, Query()] = None,
    names: Annotated[str, Query()] = None,
    symbols: Annotated[str, Query()] = None,
    currencies: str = "usd",
    precision: str = "2",
):
    coin_price_url = get_url("simple/price")
    params = {
        "vs_currencies": currencies,
        "ids": ids,
        "names": names,
        "symbols": symbols,
        "precision": precision,
    }

    client = RequestsClient(url=coin_price_url, params=params)
    response = client.get()

    return response
